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

#______________________________________

@app.route('/insert', methods=["POST"])
def insert_response():
    data = chat_gpt_response()

    if 'question' in data and 'response' in data and 'time' in data:
    
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