const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const url = require('url');

let mainWindow;

function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 1024,
    height: 768,
    webPreferences: {
      nodeIntegration: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Carga la página HTML principal
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'views', 'login.html'),
    protocol: 'file:',
    slashes: true
  }));

  // Abre las DevTools (consola de desarrollo) si es necesario
  // mainWindow.webContents.openDevTools();

  // Escucha el evento de cierre de la ventana principal
  mainWindow.on('closed', function () {
    mainWindow = null;
  });

  // Escucha eventos del proceso renderizador (vista)
  ipcMain.on('login', (event, userData) => {
    // Realiza la autenticación del usuario (comprueba las credenciales en tu backend)
    // Si la autenticación es exitosa, carga la página de inicio o dashboard
    if (userData.username === 'admin' && userData.password === 'adminpassword') {
      mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'views', 'dashboard.html'),
        protocol: 'file:',
        slashes: true
      }));
    } else {
      // Muestra un mensaje de error o realiza redirección
    }
  });

  // Otros eventos y lógica de la ventana principal
}

// Evento cuando la aplicación está lista
app.on('ready', createMainWindow);

// Evento cuando todas las ventanas están cerradas
app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Evento cuando la aplicación se activa
app.on('activate', function () {
  if (mainWindow === null) {
    createMainWindow();
  }
});
