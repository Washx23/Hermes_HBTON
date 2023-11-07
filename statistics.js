// Lógica para volver a la página de administrador
const backButton = document.getElementById('back-button');
backButton.addEventListener('click', () => {
  // Redirige de vuelta a la página de administrador (dashboard.html) o al destino deseado
  window.location.href = 'dashboard.html';
});

// Lógica para mostrar los gráficos de estadísticas (usando Chart.js como ejemplo)
const ctx = document.getElementById('bar-chart').getContext('2d');
const data = {
  labels: ['Emoción 1', 'Emoción 2', 'Emoción 3', 'Emoción 4'],
  datasets: [
    {
      label: 'Cantidad de Emociones',
      data: [25, 40, 30, 20],
      backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(75, 192, 192, 0.6)', 'rgba(255, 206, 86, 0.6)', 'rgba(54, 162, 235, 0.6)'],
      borderColor: ['rgba(255, 99, 132, 1)', 'rgba(75, 192, 192, 1)', 'rgba(255, 206, 86, 1)', 'rgba(54, 162, 235, 1)'],
      borderWidth: 1,
    },
  ],
};

new Chart(ctx, {
  type: 'bar',
  data: data,
});
