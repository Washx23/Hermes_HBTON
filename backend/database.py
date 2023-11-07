const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('hermes', 'postgres', 'hermest4', {
  host: 'localhost',
  port: 5432,
  dialect: 'postgres'
});

// Definir modelos aquí

// Inicializar la base de datos y crear tablas
async function initDB() {
  try {
    await sequelize.sync({ force: false }); // Cambiar a true para forzar la recreación de tablas
    console.log('Base de datos inicializada y tablas creadas con éxito');
  } catch (error) {
    console.error('Error al inicializar la base de datos:', error);
  }
}

module.exports = { sequelize, initDB };
