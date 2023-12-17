from flask import Flask, request, jsonify, render_template 
import json
import requests
import psycopg2
import os
from datetime import datetime
import sqlite3
import variables

from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


os.chdir(os.path.dirname(__file__))

#path_upload=os.getcwd()+'/4-Data_Engineering/Entregas/uploads'
path_upload=os.getcwd()+'\\uploads'

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/upload', methods=['POST'])
def upload_file():
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
        return 'Selecciona un archivo .py válido'
    
def connect():

    #Set up a connection to the postgres server.
    conn_string = "host="+ variables.PGEND_POINT + \
        " port="+ "5432" +" dbname="+ variables.PGDATABASE_NAME + \
        " user=" + variables.PGUSER_NAME + \
        " password="+ variables.PGPASSWORD

    conn = psycopg2.connect(conn_string)
    print("Connected!")

    # Create a cursor object
    cursor = conn.cursor()

    return conn, cursor

def chat_gpt_response(question):

    error = None
    answer = {}
    question = question["question"]

    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=variables.API_KEY_CHATGPT)

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
            question=question,
        )
        time = datetime.now()
        answer = {
            'question': question,
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

@app.route('/insert', methods=["POST"])
def insert_response():
    question = request.json

    data = chat_gpt_response(question)

    if 'question' in data and 'response' in data and 'time' in data:

        conn, cursor = connect()

        cursor.execute('''
            INSERT INTO chat (time, question, response)
            VALUES (?, ?, ?);
        ''', (data['time'], data['question'], data['response']))

        conn.commit()
        conn.close()

        return jsonify(data['response'])
    else:
        return jsonify({'error': 'JSON incorrecto'})

if __name__ == '__main__':
    app.run(debug=True)