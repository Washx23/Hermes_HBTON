const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  // Aquí puedes exponer funciones o métodos que necesites en la ventana de renderización
  sendToMain: (channel, data) => {
    ipcRenderer.send(channel, data);
  },
});
