import psycopg2
import os
import variable
from datetime import datetime

from langchain.chains import AnalyzeDocumentChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


def connect_aws():
    #Set up a connection to the postgres server.
    conn_string = "host="+ variable.PGEND_POINT + \
        " port="+ "5432" +" dbname="+ variable.PGDATABASE_NAME + \
        " user=" + variable.PGUSER_NAME + \
        " password="+ variable.PGPASSWORD

    conn = psycopg2.connect(conn_string)
    print("Connected!")

    # Create a cursor object
    cursor = conn.cursor()

    return conn, cursor

def chat_gpt_response(question):

    error = None
    answer = {}
    question = question["question"]

    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=variable.API_KEY_CHATGPT)

    qa_chain = load_qa_chain(llm, chain_type="map_reduce")

    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)

    try:
        path = f"{os.getcwd()}/../uploads"
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