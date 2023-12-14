import json
from flask import Flask, request
import sqlite3
import pickle
import pandas as pd
import os

def clean_data(data):
    columns = data.columns
    if "Unnamed: 0" in columns:
        data.drop(columns='Unnamed: 0', inplace=True)

    index = data[data["newpaper"].str.contains(r".*[a-zA-Z].*")].index  
    data.loc[index,"newpaper"] = data.loc[index,"newpaper"].str.replace("s","")
    data['newpaper'] = data['newpaper'].astype(float)
    data.rename(columns={"newpaper" : "newspaper"}, inplace=True)

    return data

def connect_db():
    conn = sqlite3.connect('advertising_new.db')

    return conn

def close_db(conn):
    conn.close()

def create_db(conn):
    cursor = conn.cursor()

    create_table = \
    """
        CREATE TABLE IF NOT EXISTS advertising (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            TV FLOAT(32),
            radio FLOAT(32),
            newspaper FLOAT(32),
            sales FLOAT(32)
        )
    """
    cursor.execute(create_table)


def add_data(conn):

    data = pd.read_csv('data/Advertising.csv')
    data = clean_data(data)

    cursor = conn.cursor()

    query =\
    """
        SELECT * FROM advertising
    """
    comp = cursor.execute(query)
    results = comp.fetchall()

    print(results)
    if not results:
        data.to_sql(name="advertising", con=conn, if_exists="replace", index=False)


def ingest_new_data(conn, data):

    cursor = conn.cursor()

    try:
        for reg in data:
            tv = float(reg[0])
            radio = float(reg[1])
            newspaper = float(reg[2])
            sales = float(reg[3])

            query_2 = \
            """
                INSERT INTO advertising (TV, radio, newspaper, sales) VALUES (?, ?, ?, ?)

            """
            cursor.execute(query_2, (tv, radio, newspaper, sales))
            conn.commit()
        
        results = {'message': 'Datos ingresados correctamente'}

    except Exception as e:
        results = {"message": f'Error entering data : {str(e)}'}
    
    return results


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    conn = connect_db()
    create_db(conn)
    add_data(conn)
    close_db(conn)
    return "Welcome to mi API conected to predict model"

@app.route('/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))
    conn = connect_db()
    cursor = conn.cursor()
    try:

        if request.json:
            results = {"TV": [], "radio": [], "newspaper": []}
            data = request.json
            input = data["data"]
            print(input)
            for reg in input:
                results["TV"].append(float(reg[0]))
                results["radio"].append(float(reg[1]))
                results["newspaper"].append(float(reg[2]))
                columns = results.keys()           
        else:
            query =\
            """
                SELECT TV, radio, newspaper FROM advertising
            """
            data = cursor.execute(query)
            results = data.fetchall()
            columns = [descripcion[0] for descripcion in cursor.description]

        print(results,columns)
        X_test = pd.DataFrame(results, columns=columns)

        prediction = model.predict(X_test)


        msg = {'prediction': f'The prediction of sales investing that amount of money in TV, radio and newspaper is: {str(round(prediction[0],2))} k €'}

    except Exception as e:
        msg = {"message": f'Error in predict data: {str(e)}'}

    close_db(conn)
    return msg

@app.route('/ingest', methods=["POST"])
def ingest_data():
    conn = connect_db()
    data = request.json
    input = data["data"]

    comp = ingest_new_data(conn, input)

    close_db(conn)
    print(comp)
    return comp

@app.route('/retrain', methods=['POST'])
def retrain():
    conn = connect_db()
    cursor = conn.cursor()
    try:
        model = pickle.load(open('data/advertising_model','rb'))

        query =\
        """
            SELECT TV, radio, newspaper, sales FROM advertising
        """
        data = cursor.execute(query)
        results = data.fetchall()

        columns = [descripcion[0] for descripcion in cursor.description]

        data = pd.DataFrame(results, columns=columns)

        X_train = data[["TV", "radio", "newspaper"]]
        y_train = data["sales"]

        model.fit(X_train, y_train)

        with open('data/advertising_model', 'wb') as archivo:
            pickle.dump(model, archivo)

        msg = {'message': 'Modelo reentrenado correctamente.'}
        
    except Exception as e:
        msg = {"message": f'Error in retrain model: {str(e)}'}
    
    close_db(conn)
    return msg

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)