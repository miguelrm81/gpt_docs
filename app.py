from flask import Flask, request, jsonify, render_template 
import json
import requests
import os
from datetime import datetime
import sqlite3
from variables import API_KEY_CHATGPT

from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


os.chdir(os.path.dirname(__file__))

app = Flask(__name__, template_folder='src/templates')

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    return "Aqui va en render template"

@app.route('/response', methods=["GET"])
def chat_gpt_response():

    error = None
    answer = {}
    # recibir informacion de html question
    #question = request.json()
    question_test = "Cuentame que endpoints tiene el archivo"

    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=API_KEY_CHATGPT)

    qa_chain = load_qa_chain(llm, chain_type="map_reduce")

    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

    try:
        path = f"{os.getcwd()}\\uploads"
        for py_file in os.listdir(path):
            python_file = py_file

        file_path = os.path.join(path, python_file)        
        with open(file_path, 'r') as file_p:
            file = file_p.read()

        response = qa_document_chain.run(
            input_document=file,
            question=question_test,
        )
        time = datetime.now()
        answer = {
            'question': question_test,
            'response': response,
            'time': time.isoformat()
        }

    except FileNotFoundError:
        error = f"El archivo '{file_path}' no fue encontrado."
    except Exception as e:
        error = f"Error al leer el archivo: {e}"

    if error:
        answer = {'error': error}

    return answer

'''{'question': 'Cuentame que endpoints tiene el archivo',
 'response': 'El archivo tiene los siguientes endpoints:\n\n1. GET \'/\': Muestra un mensaje de bienvenida y crea una tabla llamada "advertising" en una base de datos SQLite si no existe. Luego, agrega datos a la tabla si no hay resultados previos.\n\n2. GET \'/predict\': Carga un modelo de predicción guardado y obtiene los datos de prueba de la base de datos. Realiza una predicción utilizando el modelo y devuelve el resultado.\n\n3. POST \'/ingest\': Recibe datos en formato JSON y los ingiere en la base de datos.\n\n4. POST \'/retrain\': Carga un modelo de predicción guardado y obtiene los datos de entrenamiento de la base de datos. Luego, entrena el modelo nuevamente con los datos actualizados y guarda el modelo entrenado.',
 'time': '2023-12-14T16:51:52.448581'}'''

#______________________________________

@app.route('/insert', methods=["POST"])
def insert_response():
    # Recibo el
    question = request.json
    
    data = chat_gpt_response(question)

    if 'question' in data and 'response' in data and 'time' in data:
    
        '''db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor)

        cursor = db.cursor()'''

        conn = sqlite3.connect('gpt_docs.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO chat (time, question, response)
            VALUES (?, ?, ?);
        ''', (data['time'], data['question'], data['response']))

        conn.commit()
        conn.close()

        return jsonify({'success': 'Datos insertados correctamente.'})
    else:
        return jsonify({'error': 'JSON incorrecto'})

if __name__ == '__main__':
    app.run(debug=True)