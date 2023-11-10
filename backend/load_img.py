

import psycopg2
import os

# Conexión a la base de datos
conexion = psycopg2.connect(
    dbname='Hermes',
    user='postgres',
    password='user',
    host='localhost',
    port=5432,
)

cursor = conexion.cursor()

# Realizar la consulta SQL utilizando parámetros para prevenir inyección SQL
cursor.execute("SELECT frames_data FROM to_process_img WHERE id = %s", (2,))

# Obtener los datos de la imagen
row = cursor.fetchone()
cursor.close()
conexion.close()
folder_path = "C:/Users/5787/Desktop/captured_frames/"
if not os.path.exists(folder_path):
        os.makedirs(folder_path)
if row is not None:
    imagen_bytea = row[0]

    # Convertir de memoryview a bytes si es necesario
    if isinstance(imagen_bytea, memoryview):
        imagen_bytea = imagen_bytea.tobytes()

    # Verificar la firma PNG
    if imagen_bytea.startswith(b'\x89PNG\r\n\x1a\n'):
        
        # Definir la ruta de la imagen y guardar los datos
        image_path = os.path.join(folder_path, "imagen_25.png")
        with open(image_path, 'wb') as image_file:
            image_file.write(imagen_bytea)
        print(f"Imagen guardada en: {image_path}")
    else:
        print("Los datos de la imagen no tienen la firma PNG válida.")
else:
    print("No se encontró la imagen con ID 25.")

# Convertir de memoryview a bytes si es necesario
if isinstance(imagen_bytea, memoryview):
    imagen_bytea = imagen_bytea.tobytes()

# Imprimir los primeros 8 bytes de la imagen
print(imagen_bytea[:8])

# Imprimir los primeros 8 bytes en hexadecimal
print(" ".join(f"{byte:02x}" for byte in imagen_bytea[:8]))

import base64

# Suponiendo que 'imagen_bytea' es tu objeto que contiene los datos de la imagen en base64
imagen_data = imagen_bytea.decode('utf-8')  # Convertir los bytes a una cadena

# Buscar el comienzo de la información de base64, asumiendo que es una imagen PNG
base64_str_index = imagen_data.find('base64,') + len('base64,')

# Extraer solo la parte de base64 de la cadena
base64_data = imagen_data[base64_str_index:]

# Decodificar los datos de base64 a bytes
image_bytes = base64.b64decode(base64_data)

# Guardar los datos de la imagen en un archivo
file_path = 'C:/Users/5787/Desktop/captured_frames/feliz2.png'
with open(file_path, 'wb') as file:
    file.write(image_bytes)

emotions = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "neutral", 5: "sad", 6: "surprice"}