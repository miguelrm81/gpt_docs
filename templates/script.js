function consultarAPI() {
    var pregunta = document.getElementById('question').value;
    var respuestaContainer = document.getElementById('respuesta');
    // Aqui tengo que poner la funcion de los resultados de la api
    var respuestaDeLaAPI = "Respuesta de la API para: '" + pregunta + "'";

    // Mostrar la respuesta en el contenedor
    respuestaContainer.innerHTML = respuestaDeLaAPI;
}