from models import db, User, Campaign
from app import app
from werkzeug.security import generate_password_hash
from datetime import datetime  # Importa el módulo datetime para trabajar con fechas y horas

# Nombre de usuario y contraseña del administrador que deseas crear
admin_username = "nombre_del_admin"
admin_password = "contraseña_segura"
admin_role = "admin"

# Crear una instancia del contexto de la aplicación
app_ctx = app.app_context()
app_ctx.push()

# Buscar al administrador por su nombre de usuario
admin = User.query.filter_by(username=admin_username).first()

if not admin:
    # Si el administrador no se encuentra, créalo con una contraseña segura y un rol
    hashed_password = generate_password_hash(admin_password)
    nuevo_admin = User(username=admin_username, password=hashed_password, role=admin_role)
    db.session.add(nuevo_admin)
    db.session.commit()
    admin = nuevo_admin

# Generar la marca de tiempo actual para created_at
current_time = datetime.utcnow()

# Utilizar el ID del administrador y la marca de tiempo para crear una nueva campaña
nueva_campania = Campaign(
    admin_id=admin.id,
    title="Título de la Campaña",
    description="Descripción de la Campaña",
    video_url="https://www.ejemplo.com/video",
    created_at=current_time
)

# Agregar la campaña a la sesión de la base de datos
db.session.add(nueva_campania)
db.session.commit()

# Pop el contexto de la aplicación después de completar las operaciones de base de datos
app_ctx.pop()
