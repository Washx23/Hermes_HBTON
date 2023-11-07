const { ipcRenderer } = require('electron');

// Manejar el evento de cerrar sesión
const logoutButton = document.getElementById('logout-button');
logoutButton.addEventListener('click', () => {
  // Enviar una señal al proceso principal para cerrar la sesión
  ipcRenderer.send('logout');
});

// Manejar el evento de clic en el botón "Agregar Nueva Campaña"
const addCampaignForm = document.getElementById('add-campaign-form');
addCampaignForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const campaignName = document.getElementById('campaign-name').value;

  // Enviar una señal al proceso principal para agregar una nueva campaña
  ipcRenderer.send('add-campaign', campaignName);
});

// Escuchar eventos del proceso principal (si se espera recibir señales desde el proceso principal)
ipcRenderer.on('some-event-from-main', (event, data) => {
  // Realizar acciones en respuesta a eventos del proceso principal
});
