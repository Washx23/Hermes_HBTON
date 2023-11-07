import sendImages from "../websocket/socket";

function openWebcam() {
  setCameraOpen(true);
  const video = document.getElementById("video") as HTMLVideoElement;
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      video.srcObject = stream;
      video.play();
      video.style.transform = "scaleX(-1)";
      let intervalId: NodeJS.Timeout;
      obtainfps(video, intervalId);
    })
    .catch((error) => {
      console.log("Error accessing webcam: " + error.toString());
    });
}

function obtainfps(video: HTMLVideoElement, intervalId: NodeJS.Timeout) {
  intervalId = setInterval(() => {
    const canvas = document.getElementById("canvas") as HTMLCanvasElement;
    const context = canvas.getContext("2d");
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL("image/jpeg");
    sendImages(imageData, WichEndPoint);
  }, 200);
}

function closeWebcam() {
  const video = document.getElementById("video") as HTMLVideoElement;
  video.pause();
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-ignore
  video.srcObject?.getTracks().forEach((track) => {
    track.stop();
  });
  video.srcObject = null;
  clearInterval(intervalId);
  setCameraOpen(false);
  //location.reload()
}
