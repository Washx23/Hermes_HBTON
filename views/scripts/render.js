document.addEventListener('DOMContentLoaded', () => {
    const userStartButton = document.getElementById('user-start-btn');
    const guestStartButton = document.getElementById('guest-start-btn');
  
    userStartButton.addEventListener('click', () => {
      // Suponiendo que tengas un archivo llamado 'user.html' en el directorio 'pages'
      shell.openPath('c:/Users/Washington/Desktop/Hermes_alpha/index.html');
    });
  
    guestStartButton.addEventListener('click', () => {
      // Suponiendo que tengas un archivo llamado 'guest.html' en el directorio 'pages'
      shell.openPath('./index.html');
    });
  });