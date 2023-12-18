from flask import Flask, request, jsonify, render_template
from functions import connect_aws, chat_gpt_response
import json
from psycopg2 import sql
import os

os.chdir(os.path.dirname(__file__))
app = Flask(__name__, template_folder='../src/templates')

path_upload=os.getcwd()+'/../uploads'

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    
    for exists_file in os.listdir(path_upload):
        if exists_file:
            rem_filename = os.path.join(path_upload, exists_file)
            os.remove(rem_filename)

    if 'file' not in request.files:
        return 'No se ha enviado ningún archivo'

    file = request.files['file']

    if file.filename == '':
        return 'No se ha seleccionado ningún archivo'

    if file and file.filename.endswith('.py'):
        filename = os.path.join(path_upload, file.filename)
        file.save(filename)
        print(filename)
        return 'Archivo cargado con éxito en la carpeta "uploads"'
    else:
        return f'Selecciona un archivo .py válido'

@app.route('/insert', methods=["POST"])
def insert_response():
    question = request.json

    data = chat_gpt_response(question)

    if 'question' in data and 'response' in data and 'time' in data:

        conn, cursor = connect_aws()

        cursor.execute('''
            INSERT INTO chat (time, question, response)
            VALUES (%s, %s, %s);
        ''', (data['time'], data['question'], data['response']))

        conn.commit()
        conn.close()

        return jsonify(data['response'])
    else:
        return jsonify({'error': 'JSON incorrecto'})
    
@app.route('/record', methods=["GET"])
def record_aws():
    try:
        conn, cursor = connect_aws()

        query_menu = sql.SQL("""
        SELECT * FROM chat;
        """)

        cursor.execute(query_menu)

        res = []

        data = cursor.fetchall()

        for row in data:
            res.append({
                'id': row[0],
                'time': row[1],
                'question': row[2],
                'response': row[3]
            })

        json_data = json.dumps(res, indent=2)

        cursor.close()  
        conn.close()

        return json_data
    except Exception as e:
        return jsonify({'error': f'Conexion fallida con el historial {e}'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)