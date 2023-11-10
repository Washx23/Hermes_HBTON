window.addEventListener('DOMContentLoaded', () => {
  // Declaraciones y asignaciones iniciales
  const videoElement = document.getElementById('videoElement');
  const startButton = document.getElementById('startButton');
  const stopButton = document.getElementById('stopButton');
  let videoStream;
  let captureInterval;
  let videoId; // Declarar videoId aquí para que sea accesible en todas las funciones

  // Funciones
  function getVideoIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('videoId');
  }

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
    // Aquí puedes hacer lo que necesites con frameData
  }

});