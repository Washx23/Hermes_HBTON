from flask import request, jsonify
from router import router
from router.utils import get_connection
# from ultralytics import YOLO
from PIL import Image
from collections import Counter
import random
import os
import json
import base64
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)


@router.route("/load_img/<path:user_id>", methods=["GET"])
def load_img(user_id):
    try:
        db = get_connection()
        cur = db.cursor()

        cur.execute("SELECT frames_data FROM to_process_img WHERE user_id = %s", (user_id,))
        row = cur.fetchone()

        if row is None:
            return jsonify({"error": f"No se encontró la imagen con ID {user_id}."}), 404

        imagen_bytea = row[0]

        # Intenta decodificar los datos de la imagen
        try:
            image_bytes = base64.b64decode(imagen_bytea)
        except Exception as e:
            logging.error(f"Error al decodificar la imagen: {e}")
            return jsonify({"error": "Error al decodificar la imagen."}), 500

        folder_path = f"images/captured_frames/{user_id}"
        os.makedirs(folder_path, exist_ok=True)

        image_path = os.path.join(folder_path, f"imagen_{random.randint(1, 100)}.png")
        with open(image_path, 'wb') as image_file:
            image_file.write(image_bytes)

        return jsonify({"message": f"Imagen guardada en: {image_path}"}), 200

    except Exception as e:
        logging.error(f"Error al cargar la imagen: {e}")
        return jsonify({"error": f"Hubo un problema al cargar la imagen: {e}"}), 500
    finally:
        cur.close()
        db.close()

# @router.route("/load_model/<int:user_id>")
# def get_model(user_id):
#     def folder_load(folder_path, height=48, width=48):
#         imagenes = []
#         new_folder_path = 'images/to_process_images'
#         if not os.path.exists(new_folder_path):
#             os.makedirs(new_folder_path)

#         for filename in os.listdir(folder_path):
#             if filename.endswith(".jpg") or filename.endswith(".png"):
#                 img_path = os.path.join(folder_path, filename)
#                 imagenes.append(img_path)

#         for counter, img_path2 in enumerate(imagenes):  # Utilizamos enumerate para obtener un contador único
#             with Image.open(img_path2) as img:
#                 img_resized = img.resize((height, width))

#                 file_name, extension = os.path.splitext(os.path.basename(img_path2))
#                 # Reemplaza espacios con guiones bajos y elimina caracteres no deseados
#                 file_name = file_name.replace(" ", "_").replace("-", "_")
#                 new_path = os.path.join(new_folder_path, f'{file_name}_{counter}_{height}x{width}{extension}')
#                 img_resized.save(new_path)

#         return new_folder_path
    
#     folder_load("images_/captured_frames/{}".format(user_id))
    
    
#     try:
#         model = YOLO('./models/emilio_v1.pt')
#         class_ids = []
#         image_folder = "images_/captured_frames/{}".format(user_id)

#         for filename in os.listdir(image_folder):
#             if filename.endswith(".jpg") or filename.endswith('.png'):     
#                 results = model(Image.open(os.path.join(image_folder, filename)))

#                 for result in results:
#                     boxes = result.boxes.cpu().numpy()
#                     class_id = boxes.cls[0]

#                     try:
#                         float_id = float(class_id)
#                         int_id = int(float_id)
#                         class_ids.append(int_id)
#                     except ValueError:
#                         print("algo salió mal")

#         filename = "emotion_results_{}.json".format(user_id)

#         if os.path.exists(filename):
#             with open(filename, mode='r') as f:
#                 prev_data = json.load(f)

#                 prev_data.extend(class_ids)

#             with open(filename, mode='w') as actualized_file:
#                 json.dump(prev_data, actualized_file)
#         else:
#             with open(filename, mode='w') as new_file:
#                 json.dump(class_ids, new_file)

#         return jsonify("el archivo JSON ha sido creado correctamente")

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"error": "Hubo un problema durante el procesamiento de las imágenes."}), 500

@router.route("/set_stadistics/<int:user_id>")
def get_results(user_id):
    filename= "emotion_results_{}.json".format(user_id)
    
    emotions_dict = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "neutral", 5: "sad", 6: "surprice"}
    
    try:
        with open(filename, mode='r') as file_read:
            data=json.load(filename)
            
        counter = Counter(data)
        results = []
        
        for emotion_id, count in counter.items():
            emotion = emotions_dict[emotion_id]
            average = count / len(data)
            print(f'El promedio de {emotion} es: {average:.2f}')
            results.append(f'El promedio de {emotion} es: {average:.2f}')
            
        
        with open('resultados.txt', 'w') as data_to_save:
            data_to_save.write('\n'.join(results))
        
        return jsonify("resultados txt ha sido creado correctamente")

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Hubo un problema durante el procesamiento de las imágenes."}), 500
        
    
@router.route("/send_mail/<int:user_id>/<int:videostream_id>", methods=['GET'])
def send_email(user_id):
    def get_email(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT email FROM user_basics WHERE id={user_id}")
        email = cursor.fetchone()
        cursor.close()
        conn.close()
        return email
    
    gmail_user = 'hermestrimegisto4@gmail.com'  # Reemplaza esto por tu correo electrónico de Gmail
    gmail_password = 'cycm pdlp hkke ixlj'
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = 'washingtonc0023@gmail.com'  # Reemplaza esto por el correo electrónico del destinatario
        msg['Subject'] = 'Resultados'

        # Adjuntar el archivo de texto al correo electrónico
        with open('resultados.txt', 'r') as f:
            attach_file = MIMEText(f.read(), 'plain')
            attach_file.add_header('Content-Disposition', 'attachment', filename=str('result.txt')) 
            msg.attach(attach_file)

        text = msg.as_string()
        server.sendmail(gmail_user, 'washingtonc0023@gmail.com', text)  # Reemplaza esto por el correo electrónico del destinatario
        server.close()
        jsonify('correo enviado')
    except Exception as e:
        logging.error(f"Error al enviar el correo electrónico: {e}")
        return jsonify({"error": f"Algo salió mal: {str(e)}"}), 500
