from models import User, Campaign, Comment, Statistic
from models import db
from flask import request
from flask_restful import Resource, Api
from flask import Flask
import psycopg2
from flask_sqlalchemy import SQLAlchemy

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

# # Función para conectar a la base de datos PostgreSQL
# def connect_to_database():
#     conn = psycopg2.connect(**db_config)
#     return conn
@app.route('/')
def home():
    return "¡Bienvenido a la página de inicio de la aplicación!"

# Recurso y rutas para Usuarios
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get(user_id)
            if user:
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "role": user.role,
                    "age": user.age,
                    "gender": user.gender,
                    "location": user.location
                }
                return user_data
            else:
                return {"message": "Usuario no encontrado"}, 404
        else:
            users = User.query.all()
            user_list = [{"id": user.id, "username": user.username, "role": user.role, "age": user.age, "gender": user.gender, "location": user.location} for user in users]
            return user_list

    def post(self):
        data = request.get_json()
        user = User(username=data["username"], password=data["password"], role=data["role"], age=data["age"], gender=data["gender"], location=data["location"])
        db.session.add(user)
        db.session.commit()
        return {"message": "Usuario creado con éxito"}, 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.get_json()
            user.username = data["username"]
            user.password = data["password"]
            user.role = data["role"]
            user.age = data["age"]
            user.gender = data["gender"]
            user.location = data["location"]
            db.session.commit()
            return {"message": "Usuario actualizado con éxito"}
        else:
            return {"message": "Usuario no encontrado"}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "Usuario eliminado con éxito"}
        else:
            return {"message": "Usuario no encontrado"}, 404

# Recurso y rutas para Campañas
class CampaignResource(Resource):
    def get(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            campaign_data = {
                "id": campaign.id,
                "admin_id": campaign.admin_id,
                "title": campaign.title,
                "description": campaign.description,
                "video_url": campaign.video_url,
                "created_at": campaign.created_at
            }
            return campaign_data
        else:
            return {"message": "Campaña no encontrada"}, 404

    def post(self):
        data = request.get_json()
        campaign = Campaign(admin_id=data["admin_id"], title=data["title"], description=data["description"], video_url=data["video_url"])
        db.session.add(campaign)
        db.session.commit()
        return {"message": "Campaña creada con éxito"}, 201

    def put(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            data = request.get_json()
            campaign.admin_id = data["admin_id"]
            campaign.title = data["title"]
            campaign.description = data["description"]
            campaign.video_url = data["video_url"]
            db.session.commit()
            return {"message": "Campaña actualizada con éxito"}
        else:
            return {"message": "Campaña no encontrada"}, 404

    def delete(self, campaign_id):
        campaign = Campaign.query.get(campaign_id)
        if campaign:
            db.session.delete(campaign)
            db.session.commit()
            return {"message": "Campaña eliminada con éxito"}
        else:
            return {"message": "Campaña no encontrada"}, 404

# Recursos y rutas para Comentarios
class CommentResource(Resource):
    def get(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            # Serializa el comentario y devuelve los datos en formato JSON
            return {"id": comment.id, "user_id": comment.user_id, "campaign_id": comment.campaign_id, "comment": comment.comment, "created_at": comment.created_at}
        else:
            return {"message": "Comentario no encontrado"}, 404

    def post(self):
        data = request.get_json()
        comment = Comment(user_id=data["user_id"], campaign_id=data["campaign_id"], comment=data["comment"])
        db.session.add(comment)
        db.session.commit()
        return {"message": "Comentario creado con éxito"}, 201

    def put(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            data = request.get_json()
            comment.user_id = data["user_id"]
            comment.campaign_id = data["campaign_id"]
            comment.comment = data["comment"]
            db.session.commit()
            return {"message": "Comentario actualizado con éxito"}
        else:
            return {"message": "Comentario no encontrado"}, 404

    def delete(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return {"message": "Comentario eliminado con éxito"}
        else:
            return {"message": "Comentario no encontrado"}, 404

# Recursos y rutas para Estadísticas
class StatisticResource(Resource):
    def get(self, statistic_id):
        statistic = Statistic.query.get(statistic_id)
        if statistic:
            # Serializa la estadística y devuelve los datos en formato JSON
            return {"id": statistic.id, "campaign_id": statistic.campaign_id, "user_id": statistic.user_id, "emotion": statistic.emotion, "timestamp": statistic.timestamp}
        else:
            return {"message": "Estadística no encontrada"}, 404

    def post(self):
        data = request.get_json()
        statistic = Statistic(campaign_id=data["campaign_id"], user_id=data["user_id"], emotion=data["emotion"], timestamp=data["timestamp"])
        db.session.add(statistic)
        db.session.commit()
        return {"message": "Estadística creada con éxito"}, 201

    def put(self, statistic_id):
        statistic = Statistic.query.get(statistic_id)
        if statistic:
            data = request.get_json()
            statistic.campaign_id = data["campaign_id"]
            statistic.user_id = data["user_id"]
            statistic.emotion = data["emotion"]
            statistic.timestamp = data["timestamp"]
            db.session.commit()
            return {"message": "Estadística actualizada con éxito"}
        else:
            return {"message": "Estadística no encontrada"}, 404

    def delete(self, statistic_id):
        statistic = Statistic.query.get(statistic_id)
        if statistic:
            db.session.delete(statistic)
            db.session.commit()
            return {"message": "Estadística eliminada con éxito"}
        else:
            return {"message": "Estadística no encontrada"}, 404

# Agregar los recursos a las rutas
api.add_resource(UserResource, '/api/user', '/api/user/<int:user_id>')
api.add_resource(CampaignResource, '/api/campaign', '/api/campaign/<int:campaign_id>')

if __name__ == '__main__':
    app.run()