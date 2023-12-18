import os
import json
import requests

PATH_UPLOAD=os.getcwd()+'\\..\\uploads'

def test_insert_question():
    url = 'http://127.0.0.1:5000/insert'  
    data = {"question": "Resume el archivo python"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert any(isinstance(value, str) for value in response.json())

def test_get_record():
    url = 'http://127.0.0.1:5000/record'  
    response = requests.get(url)

    try:
        json_data = response.json()[0]
    except json.JSONDecodeError:
        assert False, "El texto no es un JSON válido."

    # Verificar la estructura del JSON
    assert isinstance(json_data, dict), "Se esperaba un objeto JSON."
    assert response.status_code == 200
    assert isinstance(json_data["id"], int), "La clave 'id' debe ser un entero."
    assert isinstance(json_data["time"], str), "La clave 'time' debe ser un entero."
    assert isinstance(json_data["question"], str), "La clave 'question' debe ser una cadena de caracteres."
    assert isinstance(json_data["response"], str), "La clave 'response' debe ser una cadena de caracteres."

