const { BrowserWindow } = require('electron').remote;

document.getElementById('open-admin').addEventListener('click', () => {
  const adminWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true
    }
  });
  adminWindow.loadFile('views/admin.html');
});



document.addEventListener('DOMContentLoaded', () => {
  // Agregar Producto
  const productForm = document.getElementById('product-form');
  productForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion').value;
    const video = document.getElementById('video').value;

    ipcRenderer.send('add-product', { nombre, descripcion, video });
  });

  // Editar Producto
  const editProductForm = document.getElementById('edit-product-form');
  const productDropdown = document.getElementById('product-dropdown');
  editProductForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const selectedProduct = productDropdown.value;
    const nuevoNombre = document.getElementById('edit-nombre').value;
    const nuevaDescripcion = document.getElementById('edit-descripcion').value;
    const nuevoVideo = document.getElementById('edit-video').value;

    ipcRenderer.send('edit-product', { id: selectedProduct, nombre: nuevoNombre, descripcion: nuevaDescripcion, video: nuevoVideo });
  });

  // Eliminar Producto
  const deleteProductForm = document.getElementById('delete-product-form');
  const deleteProductDropdown = document.getElementById('delete-product-dropdown');
  deleteProductForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const selectedProduct = deleteProductDropdown.value;

    ipcRenderer.send('delete-product', selectedProduct);
  });

  // Otros eventos y lógica para el administrador
});

ipcRenderer.on('product-added', (event, result) => {
  // Manejar la confirmación de agregar un producto
  // Puedes actualizar la lista de productos u ofrecer un mensaje de éxito
});

ipcRenderer.on('product-list', (event, products) => {
  // Actualizar la interfaz para mostrar la lista de productos
  const productList = document.getElementById('product-list');
  productList.innerHTML = '';

  products.forEach((product) => {
    const listItem = document.createElement('li');
    listItem.textContent = product.nombre;
    productList.appendChild(listItem);
  });
});

ipcRenderer.send('get-products'); // Solicitar la lista de productos al cargar

// Otros eventos y lógica para el administrador
