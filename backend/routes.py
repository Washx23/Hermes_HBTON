from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from models import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:hermest4@localhost:5432/hermes"  # Conexión a la base de datos PostgreSQL

db.init_app(app)

api = Api(app)

#  Define la configuración de la base de datos PostgreSQL
db_config = {
     "host": "localhost",
     "port": "5432",
     "database": "hermes",
     "user": "postgres",
     "password": "hermest4"
}

# Configura Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# # Configura Flask-JWT-Extended
# app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Reemplaza con tu clave secreta
# jwt = JWTManager(app)

# # Define el modelo de datos del usuario (debe extender UserMixin para usar Flask-Login)
# class User(db.Model, UserMixin):
#     # Definición de la tabla de Usuarios

# Implementa una función para cargar un usuario por su ID
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))



# Ruta de autenticación para administradores
@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Realiza la autenticación del administrador (debes implementar tu lógica de autenticación aquí)
    admin = User.query.filter_by(username=username, password=password).first()
    
    if admin:
        login_user(admin)  # Inicia la sesión del administrador
        return {"message": "Inicio de sesión exitoso para el administrador"}

    return {"message": "Credenciales incorrectas"}, 401

# Ruta de autenticación para usuarios invitados
@app.route('/guest_login', methods=['POST'])
def guest_login():
    data = request.get_json()
    age = data.get('age')
    gender = data.get('gender')
    location = data.get('location')

    # Realiza la autenticación de usuarios invitados (debes implementar tu lógica de autenticación aquí)
    # Si las credenciales son válidas, genera un token JWT para el usuario invitado
    access_token = create_access_token(identity={"age": age, "gender": gender, "location": location})
    
    return {"access_token": access_token}

# Ruta protegida para usuarios invitados que requieren autenticación JWT
@app.route('/guest_protected', methods=['GET'])
@jwt_required
def guest_protected_route():
    user_identity = current_user
    return {"message": f"Ruta protegida para usuario invitado: {user_identity}"}

if __name__ == '__main__':
    app.run()
