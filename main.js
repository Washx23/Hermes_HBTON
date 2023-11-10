const { app, BrowserWindow, ipcMain } = require('electron');
const { saveFrame } = require('./database'); // Asegúrate de que este módulo esté implementado correctamente
const path = require('path');

let mainWindow;

function createWindow() {
  // Crear la ventana del navegador principal
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 1000,
    webPreferences: {
      webSecurity: false, // Deshabilita la seguridad web para el desarrollo local, no recomendado para producción
      nodeIntegration: false, // Desactiva la integración de Node en el contexto de renderizado
      contextIsolation: true, // Protege contra la manipulación de objetos globales y aislamiento de contextos
      preload: path.join(__dirname, 'preload.js') // Especifica un script de precarga
    }
  });

  // y carga el archivo index.html de la aplicación.
  mainWindow.loadFile('./index.html'); // Asegúrate de que este archivo exista en la ruta correcta

  // Abre las herramientas de desarrollo.
  // mainWindow.webContents.openDevTools(); // Descomenta si quieres abrir las herramientas de desarrollo por defecto
}

app.whenReady().then(createWindow);

// Cierra la aplicación cuando todas las ventanas están cerradas, excepto en macOS.
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});

// En macOS, recarga la ventana de la aplicación cuando el icono del dock es clickeado y no hay otras ventanas abiertas.
app.on('activate', function () {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// Manejo de IPC para guardar datos de un 'frame'
// ipcMain.on('save-frame', async (event, frameData) => {
//   try {
//     await saveFrame(frameData); // Implementa esta función en el módulo 'database'
//     event.reply('save-frame-reply', 'Frame saved successfully');
//   } catch (error) {
//     event.reply('save-frame-reply', `Error saving frame: ${error.message}`);
//   }
// });

ipcMain.on('save-frame', async (event, frameData, userId) => {
  try {
    const result = await saveFrame(frameData, userId);
    event.reply('save-frame-reply', { status: 'success', result: result });
  } catch (error) {
    event.reply('save-frame-reply', { status: 'error', message: error.message });
  }
});
