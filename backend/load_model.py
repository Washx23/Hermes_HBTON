#!/usr/bin/python3
import json
import os
from ultralytics import YOLO
from PIL import Image

folder_path = "C:/Users/5787/Desktop/captured_frames/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def folder_load(folder_path, height=48, width=48):
    imagenes = []
    new_folder_path = 'C:/Users/5787/Desktop/captured_frames/resized_imgs'
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


def load_model(model_path, image_folder):
    model = YOLO(model_path)
    class_ids = []
        
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith('.png'):     
            results = model(Image.open(os.path.join(image_folder, filename)))

            for result in results:
                boxes = result.boxes.cpu().numpy()
                class_id = boxes.cls[0]

                try:
                    float_id = float(class_id)
                    int_id = int(float_id)
                    class_ids.append(int_id)
                except ValueError:
                    print("algo salio mal")
    
    filename = "emotion_results.json"

    if os.path.exists(filename):
        with open(filename, mode='r') as f:
            prev_data = json.load(f)

            prev_data.extend(class_ids)

        with open(filename, mode='w') as actualized_file:
            json.dump(prev_data, actualized_file)
    else:
        with open(filename, mode='w') as new_file:
            json.dump(class_ids, new_file)
new_folder_path = folder_load(folder_path)
load_model("emilio_v1.pt",new_folder_path)