window.addEventListener('DOMContentLoaded', () => {
  const videoId = localStorage.getItem('videoId');
  if (videoId) {
    console.log('El videoId recuperado del almacenamiento local es:', videoId);
  } else {
    console.log('No se encontró el videoId en el almacenamiento local.');
  }

  const videoElement = document.getElementById('videoElement');
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  let videoStream;
  let captureInterval;

  startButton.addEventListener('click', () => {
    startCapturing();
  });

  stopButton.addEventListener('click', () => {
    stopCapturing();
    startProcess(videoId);
  });

  async function startCapturing() {
    videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = videoStream;
    captureInterval = setInterval(captureFrame, 1000);
  }

  function captureFrame() {
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    const frameData = canvas.toDataURL('image/png');
    window.api.saveFrame(frameData, videoId);
  }

  function stopCapturing() {
    clearInterval(captureInterval);
    let tracks = videoElement.srcObject.getTracks();
    tracks.forEach(track => track.stop());
    videoElement.srcObject = null;
  }

  function startProcess(videoId) {
    loadUserImage(videoId)
      .then(() => processImageWithModel(videoId))
      .then(() => setStatistics(videoId))
      .then(() => sendEmail(videoId))
      .catch(error => {
        console.error('Error en el proceso:', error);
      });
  }

  function loadUserImage(videoId) {
    return fetch(`http://localhost:5000/load_img/${videoId}`)
      .then(response => response.ok ? response.json() : Promise.reject('Error al cargar la imagen'))
      .then(data => {
        console.log('Imagen cargada:', data);
        return data;
      })
      .catch(error => {
        console.error('Error al cargar la imagen:', error);
      });
  }

  function processImageWithModel(videoId) {
    return fetch(`http://localhost:5000/load_model/${videoId}`)
      .then(response => response.json())
      .then(data => {
        console.log('Modelo procesado:', data);
        return data;
      })
      .catch(error => {
        console.error('Error al procesar la imagen con el modelo:', error);
      });
  }

  function setStatistics(videoId) {
    return fetch(`http://localhost:5000/set_statistics/${videoId}`)
      .then(response => {
        if (!response.ok) {
            throw new Error('Respuesta del servidor no fue exitosa');
        }
        return response.json();
      })
      .then(data => {
        console.log('Estadísticas establecidas:', data);
        return data;
      })
      .catch(error => {
        console.error('Error al establecer estadísticas:', error.message);
      });
}


function sendEmail(videoId) {
  return fetch(`http://localhost:5000/send_mail/${videoId}`)
    .then(response => {
      if (!response.ok) {
          // Lanza un error si la respuesta del servidor no es exitosa
          throw new Error('Respuesta del servidor no fue exitosa');
      }
      return response.json();
    })
    .then(data => {
      console.log('Correo electrónico enviado:', data);
      return data;
    })
    .catch(error => {
      console.error('Error al enviar el correo electrónico:', error.message);
    });
  }
});
