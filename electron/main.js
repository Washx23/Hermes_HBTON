const { app, BrowserWindow, ipcMain } = require('electron');
const { Client } = require('pg');
const path = require('path');
const url = require('url');

let mainWindow; // Utiliza una variable para hacer seguimiento de la ventana principal

// Configura la conexión a PostgreSQL
const db = new Client({
  user: 'tu_usuario',
  password: 'tu_contraseña',
  host: 'localhost',
  port: 5432,
  database: 'tu_base_de_datos'
});

db.connect(); // Conectar a la base de datos PostgreSQL

app.on('ready', () => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });

  mainWindow.loadFile('index.html');

  mainWindow.webContents.openDevTools();

  mainWindow.on('closed', () => {
    mainWindow = null; // Cierra la ventana en lugar de asignar null
  });

  // Agregar el resto de las operaciones de ventana principal aquí
});

ipcMain.on('load-module', (event, moduleName) => {
  try {
    // Realizar la carga del módulo aquí, si es necesario
    const loadedModule = require(moduleName);

    // Enviar el módulo cargado al proceso de representación
    event.sender.send('module-loaded', loadedModule);
  } catch (error) {
    console.error('Error al cargar el módulo:', error);
    event.sender.send('module-loaded', null);
  }
});
// Escuchar eventos del proceso de representación

ipcMain.on('add-product', async (event, productData) => {
  try {
    const { nombre, descripcion, video } = productData;
    await db.none('INSERT INTO productos (nombre, descripcion, video) VALUES($1, $2, $3)', [nombre, descripcion, video]);
    event.sender.send('product-added', { message: 'Producto agregado con éxito' });
  } catch (error) {
    console.error('Error al agregar un producto:', error);
    event.sender.send('product-added', { error: 'Error al agregar el producto' });
  }
});

ipcMain.on('get-products', async (event) => {
  try {
    const products = await db.any('SELECT * FROM productos');
    event.sender.send('product-list', products);
  } catch (error) {
    console.error('Error al obtener la lista de productos:', error);
    event.sender.send('product-list', []);
  }
});

ipcMain.on('edit-product', async (event, productData) => {
  try {
    const { id, nombre, descripcion, video } = productData;
    await db.none('UPDATE productos SET nombre=$1, descripcion=$2, video=$3 WHERE id=$4', [nombre, descripcion, video, id]);
    event.sender.send('product-edited', { message: 'Producto editado con éxito' });
  } catch (error) {
    console.error('Error al editar el producto:', error);
    event.sender.send('product-edited', { error: 'Error al editar el producto' });
  }
});

ipcMain.on('delete-product', async (event, productId) => {
  try {
    await db.none('DELETE FROM productos WHERE id=$1', productId);
    event.sender.send('product-deleted', { message: 'Producto eliminado con éxito' });
  } catch (error) {
    console.error('Error al eliminar el producto:', error);
    event.sender.send('product-deleted', { error: 'Error al eliminar el producto' });
  }
});

// Otros eventos y lógica de la ventana principal
