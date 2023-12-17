# gpt_docs

# 1. Aplicación de Consultas de Documentos mediante GPT
## Descripción
El proyecto tiene como objetivo desarrollar una aplicación en Python que permita realizar consultas específicas sobre documentos cargados utilizando un agente de Langchain y la API de OpenAI. La aplicación ofrece tanto una interfaz de usuario para cargar documentos y realizar preguntas como un endpoint accesible mediante peticiones HTTP para automatizar consultas.

## Características Principales
### 1. Interfaz de Usuario:

Implementación de un frontend con un formulario que permita a los usuarios cargar documentos y realizar preguntas de manera interactiva.
### 2. Endpoint de API:

Desarrollo de un endpoint que acepte peticiones con un documento y una pregunta, y devuelva una respuesta. Esto facilita la integración con otras aplicaciones o sistemas externos.
### 3. Conexiones con Langchain y OpenAI:

Integración de conexiones y flujos de información para realizar llamadas a las APIs de Langchain y OpenAI. Se espera obtener información detallada del documento y respuestas coherentes a las preguntas realizadas.
### 4. Base de Datos en AWS:

Utilización de una base de datos alojada en AWS para almacenar las preguntas realizadas y sus respuestas asociadas. Esto permite el seguimiento y la referencia de consultas anteriores.
### 5. Dockerización y Despliegue:

Creación de un repositorio en DockerHub con la imagen de la aplicación para facilitar su despliegue. Esto garantiza la portabilidad y escalabilidad de la aplicación.
## Pasos Previos
Antes de comenzar con la implementación de la aplicación, asegúrate de tener configuradas las siguientes herramientas y servicios:

1. Cuenta en Langchain con acceso a las API necesarias.
2. Claves de API de OpenAI para utilizar su servicio GPT.
3. Cuenta de AWS para la creación y configuración de la base de datos.
## Instrucciones de Despliegue
### 1. Clonar el Repositorio:

git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto

### 2. Configuración del Entorno:

Configura las variables de entorno necesarias, como las claves de API de Langchain y OpenAI, así como las credenciales de AWS para acceder a la base de datos.
### 3. Instalación de Dependencias:

pip install -r requirements.txt
### 4. Ejecución de la Aplicación:

python app.py
### 5. Acceso a la Interfaz de Usuario:

Abre tu navegador y visita http://localhost:5000 para interactuar con la interfaz de usuario.
### 6. Uso del Endpoint de API:

Realiza peticiones HTTP al endpoint para automatizar consultas. Ejemplo:

curl -X POST -H "Content-Type: application/json" -d '{"documento": "Contenido del documento", "pregunta": "¿Cuál es la pregunta?"}' http://localhost:5000/api/consultar
### 7. Despliegue con Docker:

Construye la imagen Docker y súbelo a DockerHub.

docker build -t tu-usuario/tu-proyecto:latest .
docker push tu-usuario/tu-proyecto:latest
Ahora, otros usuarios pueden desplegar la aplicación utilizando Docker.
