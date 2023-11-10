// // preload.js
// const { contextBridge, ipcRenderer } = require('electron');

// contextBridge.exposeInMainWorld('api', {
//   saveFrame: (frameData) => {
//     ipcRenderer.send('save-frame', frameData);
//   }
// });

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  saveFrame: (frameData, userId) => ipcRenderer.send('save-frame', frameData, userId),
  onFrameSaved: (callback) => {
    ipcRenderer.on('save-frame-reply', (event, response) => callback(response));
  }
});
