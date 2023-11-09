// camera.js
window.addEventListener('DOMContentLoaded', () => {
    const videoElement = document.getElementById('videoElement');
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
  
    let videoElement1 = document.getElementById('video1');
    let videoElement2 = document.getElementById('video2');
    let videoStream;
    let captureInterval;
  
    startButton.addEventListener('click', () => {
      startCapturing();
    });
  
    stopButton.addEventListener('click', () => {
      stopCapturing();
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
      window.api.saveFrame(frameData);
    }
  
    function stopCapturing() {
      clearInterval(captureInterval);
      let tracks = videoElement.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoElement.srcObject = null;
    }
  });
  
  
  // window.addEventListener('DOMContentLoaded', () => {
  //   const startButton = document.getElementById('startButton');
  //   const stopButton = document.getElementById('stopButton');
  
  //   let videoElement1 = document.getElementById('video1');
  //   let videoElement2 = document.getElementById('video2');
  //   let videoStream;
  //   let captureInterval;
  
  //   startButton.addEventListener('click', () => {
  //       startCapturing();
  //   });
  
  //   stopButton.addEventListener('click', () => {
  //       stopCapturing();
  //   });
  
  //   async function startCapturing() {
  //       try {
  //           videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
  //           videoElement1.srcObject = videoStream;
  //           videoElement2.src = "https://www.youtube.com/watch?v=LD8P8Mq3rVU";
            
  //           videoElement2.addEventListener('canplay', function() {
  //               this.play();
  //           });
  
  //           captureInterval = setInterval(captureFrame, 1000);
  //       } catch(err) {
  //           console.log('Error: ', err);
  //       }
  //   }
  
  //   function captureFrame() {
  //       let canvas = document.createElement('canvas');
  //       canvas.width = videoElement1.videoWidth;
  //       canvas.height = videoElement1.videoHeight;
  //       canvas.getContext('2d').drawImage(videoElement1, 0, 0);
  //       let imgDataUrl = canvas.toDataURL('image/png');
  //       // Here you can do whatever you want with imgDataUrl,
  //       // like upload it to a server or save it in local storage.
  //   }
  
  //   function stopCapturing() {
  //       clearInterval(captureInterval);
  //       let tracks = videoElement1.srcObject.getTracks();
  //       tracks.forEach(track => track.stop());
  //       videoElement1.srcObject = null;
  //   }
  // });