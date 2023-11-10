import psycopg2  

from flask import request
from flask import Flask
from flask_cors import CORS  # Asegúrate de importar CORS
from router import router

app = Flask(__name__)
CORS(app)  # Habilita CORS para la aplicación
app.url_map.strict_slashes = False

app.register_blueprint(router)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user@localhost:5432/Hermes'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    