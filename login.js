const electron = window.electron;

document.getElementById('login-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  electron.sendToMain('login', { username, password });
  // Debes recibir una respuesta del proceso principal y decidir si redirigir al dashboard
  mainWindow.loadFile('views/dashboard.html');
});
