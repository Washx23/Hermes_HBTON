# app/utils.py
import uuid

def calculate_emotion_intensity(emotion_data):
    """
    Calcula la intensidad de una emoción a partir de los datos de emociones.
    :param emotion_data: Datos de emociones (por ejemplo, una lista de valores de intensidad).
    :return: Intensidad promedio de la emoción.
    """
    if not emotion_data:
        return 0
    
    total_intensity = sum(emotion_data)
    average_intensity = total_intensity / len(emotion_data)
    return average_intensity


def generate_unique_id():
    """
    Genera un identificador único.
    :return: Identificador único generado.
    """
    unique_id = str(uuid.uuid4())
    return unique_id

# Ejemplo de uso:
unique_id = generate_unique_id()
print(unique_id)