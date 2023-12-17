function consultarAPI() {
    var pregunta = document.getElementById('question').value;
    var respuestaContainer = document.getElementById('respuesta');

    // Guardar la pregunta en un archivo JSON utilizando fetch
    guardarPreguntaEnJSON(pregunta)
        .then(() => {
            // Luego de guardar la pregunta, puedes realizar la consulta a tu API
            // Aquí tendrías tu lógica para consultar la API y mostrar la respuesta
            var respuestaDeLaAPI = "Respuesta de la API para: '" + pregunta + "'";

            // Mostrar la respuesta en el contenedor
            respuestaContainer.innerHTML = respuestaDeLaAPI;
        })
        .catch(error => {
            console.error('Error al guardar la pregunta:', error);
            respuestaContainer.innerHTML = 'Error al guardar la pregunta.';
        });
}

function guardarPreguntaEnJSON(pregunta) {
    // URL de tu endpoint en el servidor Flask para guardar la pregunta
    var guardarPreguntaURL = '/insert';

    // Configurar los datos a enviar en la solicitud
    var data = {
        question: pregunta
    };

    // Configurar la solicitud POST
    return fetch(guardarPreguntaURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al guardar la pregunta en el servidor.');
        }
    });
}