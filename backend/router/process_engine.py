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

        cur.execute("SELECT frames_data FROM to_process_img WHERE video_id = %s", (user_id,))
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

@router.route("/load_model/<int:user_id>")
def get_model(user_id):
    from ultralytics import YOLO

    def folder_load(folder_path, height=48, width=48):
        imagenes = []
        new_folder_path = 'images/to_process_images'
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            
            for filename in os.listdir(folder_path):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    img_path = os.path.join(folder_path, filename)
                    imagenes.append(img_path)

            for counter, img_path2 in enumerate(imagenes):  # Utilizamos enumerate para obtener un contador único
                with Image.open(img_path2) as img:
                    img_resized = img.resize((height, width))

                file_name, extension = os.path.splitext(os.path.basename(img_path2))
                 # Reemplaza espacios con guiones bajos y elimina caracteres no deseados
                file_name = file_name.replace(" ", "_").replace("-", "_")
                new_path = os.path.join(new_folder_path, f'{file_name}_{counter}_{height}x{width}{extension}')
                img_resized.save(new_path)

        return new_folder_path
    
    folder_load("images_/captured_frames/{}".format(user_id))
    
    
    try:
        #model = YOLO('./models/emilio_v1.pt')
        image_folder = "images_/captured_frames/{}".format(user_id)

        for filename in os.listdir(image_folder):
            if filename.endswith(".jpg") or filename.endswith('.png'):     
                """results = model(Image.open(os.path.join(image_folder, filename)))

                for result in results:
                    boxes = result.boxes.cpu().numpy()
                    class_id = boxes.cls[0]

                    try:
                        float_id = float(class_id)
                        int_id = int(float_id)
                        class_ids.append(int_id)
                    except ValueError:
                        print("algo salió mal") """
        class_ids = []
        temp_list = [4.0, 2.0, 3.0, 3.0, 3.0, 4.0, 3.0, 2.0, 3.0]
        # Agregamos la lista temp_list a class_ids
        class_ids.extend(temp_list)

        print("class_ids después de agregar temp_list:", class_ids)  # Mensaje de depuración

        filename = "emotion_results_{}.json".format(user_id)
        print("Nombre del archivo JSON:", filename)  # Mensaje de depuración

        data_to_save = class_ids
        if os.path.exists(filename):
            with open(filename, mode='r') as f:
                prev_data = json.load(f)
                print("Datos previos cargados del archivo JSON:", prev_data)  # Mensaje de depuración
            data_to_save = prev_data + class_ids

        with open(filename, mode='w') as file:
            json.dump(data_to_save, file)
            print("Datos escritos en el archivo JSON")  # Mensaje de depuración

        return jsonify("el archivo JSON ha sido creado o actualizado correctamente")

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Hubo un problema durante el procesamiento de las imágenes."}), 500
@router.route("/set_statistics/<int:user_id>", methods=['GET'])
def get_results(user_id):
    filename = "emotion_results_{}.json".format(user_id)
    print(f"Verificando el archivo JSON: {filename}")  # Depuración: Verificar la ruta del archivo

    emotions_dict = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "neutral", 5: "sad", 6: "surprise"}

    try:
        if not os.path.exists(filename):
            print(f"Archivo no encontrado: {filename}")  # Depuración: Verificar si el archivo existe
            return jsonify({"error": "Archivo JSON no encontrado"}), 404

        with open(filename, mode='r') as file_read:
            data = json.load(file_read)  
            print(f"Datos leídos del archivo JSON: {data}")  # Depuración: Verificar datos leídos

        counter = Counter(data)
        results = []

        for emotion_id, count in counter.items():
            emotion = emotions_dict.get(int(emotion_id), "unknown")
            average = count / len(data)
            print(f'El promedio de {emotion} es: {average:.2f}')  # Depuración: Mostrar cálculos
            results.append(f'El promedio de {emotion} es: {average:.2f}')

        resultados_path = 'resultados.txt'
        with open(resultados_path, 'w') as data_to_save:
            data_to_save.write('\n'.join(results))
            print(f"Resultados escritos en: {os.path.abspath(resultados_path)}")  # Depuración: Confirmar escritura

        return jsonify("resultados.txt ha sido creado correctamente")

    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return jsonify({"error": error_message}), 500
    
@router.route("/send_mail/<int:video_id>", methods=['GET'])
def send_email(video_id):
    def get_email(video_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT user_id FROM video WHERE id = {video_id}")
        user_id = cursor.fetchone()
        cursor.execute(f"SELECT email FROM user_basics WHERE id={user_id[0]}")
        email = cursor.fetchone()
        cursor.close()
        conn.close()
        return email[0] if email else None
    email = get_email(video_id)
    
    gmail_user = 'hermestrimegisto4@gmail.com'  # Reemplaza esto por tu correo electrónico de Gmail
    gmail_password = 'cycm pdlp hkke ixlj'
    
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = email  # Reemplaza esto por el correo electrónico del destinatario
        msg['Subject'] = 'Resultados'

        # Adjuntar el archivo de texto al correo electrónico
        with open('resultados.txt', 'r') as f:
            attach_file = MIMEText(f.read(), 'plain')
            attach_file.add_header('Content-Disposition', 'attachment', filename=str('result.txt')) 
            msg.attach(attach_file)

        text = msg.as_string()
        server.sendmail(gmail_user, 'washingtonc0023@gmail.com', text)  # Reemplaza esto por el correo electrónico del destinatario
        server.close()
        return jsonify({'message': 'correo enviado'})  # Asegúrate de devolver una respuesta aquí
    except Exception as e:
        logging.error(f"Error al enviar el correo electrónico: {e}")
        return jsonify({"error": f"Algo salió mal: {str(e)}"}), 500  # Devuelve una respuesta también en caso de error

    # Es importante tener un retorno final en caso de que ninguna de las anteriores se ejecute
    return jsonify({"error": "Error desconocido"}), 500