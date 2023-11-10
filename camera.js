window.addEventListener('DOMContentLoaded', () => {
  // Obtener el videoId del almacenamiento local
  const videoId = localStorage.getItem('videoId');
  if (videoId) {
    console.log('El videoId recuperado del almacenamiento local es:', videoId);
    // Puedes hacer algo con el videoId aquí
  } else {
    console.log('No se encontró el videoId en el almacenamiento local.');
    // Maneja la situación si no hay un videoId disponible
  }

  const videoElement = document.getElementById('videoElement');
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  let videoStream;
  let captureInterval;

  // Asegúrate de que cualquier función que necesite videoId se llame después de esta línea
  // para asegurarte de que videoId está definido.

  startButton.addEventListener('click', () => {
    startCapturing();
    // Si necesitas usar videoId en esta función, está disponible aquí.
    
  });

  stopButton.addEventListener('click', () => {
    stopCapturing();
    startProcess(videoId); // Asumiendo que deseas usar videoId aquí
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
    // Enviar el frame capturado al proceso principal usando la API expuesta en preload.js
    window.api.saveFrame(frameData, videoId);
    ipcRenderer.send('save-frame', { frameData, videoId });
  }

  function stopCapturing() {
    clearInterval(captureInterval);
    let tracks = videoElement.srcObject.getTracks();
    tracks.forEach(track => track.stop());
    videoElement.srcObject = null;
  }

});
 

   function loadUserImage(videoId) {
     return fetch(`http://localhost:5000/load_img/${videoId}`)
       .then(response => response.json())
       .then(data => {
         console.log('Imagen cargada:', data);
         return data;
       })
       .catch(error => {
         console.error('Error al cargar la imagen:', error);
       });
   }

    function processImageWithModel(videoI) {
      return fetch(`http:localhost:5000/load_model/${videoI}`)
        .then(response => response.json())
        .then(data => {
          console.log('Modelo procesado:', data);
          return data;
        })
        .catch(error => {
          console.error('Error al procesar la imagen con el modelo:', error);
        });
    }

    function setStatistics(videoI) {
      return fetch(`http:localhost:5000/set_stadistics/${videoI}`)
        .then(response => response.json())
        .then(data => {
          console.log('Estadísticas establecidas:', data);
          return data;
        })
        .catch(error => {
          console.error('Error al establecer estadísticas:', error);
        });
    }

    function sendEmail(videoI, videoStreamId) {
      return fetch(`http:localhost:5000/send_mail/${videoI}/${videoStreamId}`)
        .then(response => response.json())
        .then(data => {
          console.log('Correo electrónico enviado:', data);
          return data;
        })
        .catch(error => {
          console.error('Error al enviar el correo electrónico:', error);
        });
    }

    function startProcess(videoId) {
      const videoStreamId = 1;  //Este valor también debe ser dinámico según necesites

      loadUserImage(videoId)
        .then(() => processImageWithModel(videoId))
        .then(() => setStatistics(videoId))
        .then(() => sendEmail(videoId, videoStreamId))
        .catch(error => {
          console.error('Error en el proceso:', error);
        });
    }

