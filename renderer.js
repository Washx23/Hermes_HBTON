const axios = require('axios');

// URL de tu API REST en el backend Python
const apiUrl = 'http://localhost:5000/api'; // Reemplaza con la URL correcta de tu API

// Función para hacer una solicitud GET a la API
async function fetchData() {
  try {
    const response = await axios.get(`${apiUrl}/endpoint`); // Reemplaza 'endpoint' con la ruta de tu API
    const data = response.data;
    console.log('Datos de la API:', data);
    // Aquí puedes actualizar la interfaz de usuario con los datos recibidos
  } catch (error) {
    console.error('Error al hacer la solicitud GET:', error);
  }
}

// Función para hacer una solicitud POST a la API
async function postData(dataToSend) {
  try {
    const response = await axios.post(`${apiUrl}/endpoint`, dataToSend); // Reemplaza 'endpoint' con la ruta de tu API
    console.log('Respuesta de la API POST:', response.data);
    // Puedes manejar la respuesta, por ejemplo, mostrar un mensaje de éxito
  } catch (error) {
    console.error('Error al hacer la solicitud POST:', error);
  }
}

// Llama a la función fetchData para obtener datos cuando se cargue la página
fetchData();

// Ejemplo de cómo llamar a la función postData con datos para enviar
const dataToSend = { key: 'value' };
postData(dataToSend);
