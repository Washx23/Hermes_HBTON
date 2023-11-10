// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  saveFrame: (frameData, userId) => {
    ipcRenderer.send('save-frame', frameData, userId);
  }
});
