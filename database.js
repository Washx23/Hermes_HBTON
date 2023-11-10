// database.js
const { Pool } = require('pg');

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'Hermes',
  password: 'hermest4',
  port: 5432,
});

async function saveFrame(frameData, userId) {
  const query = 'INSERT INTO to_process_img(frames_data, user_id) VALUES($1, $2)';
  try {
    const res = await pool.query(query, [frameData, userId]);
    console.log('Frame guardado:', userId);
  } catch (err) {
    console.error('Error al guardar el frame:', err);
  }
}

module.exports = { saveFrame };
