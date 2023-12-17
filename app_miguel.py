from flask import Flask, request, render_template
import os

app = Flask(__name__, template_folder='templates')

path_upload=os.getcwd()+'\\uploads'

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
        with open(path_upload, 'w') as archivo_destino:
            archivo_destino.write(file)
        return 'Archivo cargado con éxito en la carpeta "uploads"'
    else:
        return 'Selecciona un archivo .py válido'

if __name__ == '__main__':
    app.run(debug=True)