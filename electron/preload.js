const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: ipcRenderer,
});
window.electron = {
    ipcRenderer: require('electron').ipcRenderer,
    // Otros módulos que necesites
  };
// preload.js
window.nodeRequire = require;
delete window.require;
delete window.exports;
delete window.module;
