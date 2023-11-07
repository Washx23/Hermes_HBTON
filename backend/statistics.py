from models import User,Statistic
from models import Statistic
from datetime import datetime

def count_emotions_by_campaign(campaign_id):
    """
    Contar la cantidad de emociones detectadas en una campaña específica.
    :param campaign_id: ID de la campaña.
    :return: Diccionario con el recuento de emociones.
    """
    statistics = Statistic.query.filter_by(campaign_id=campaign_id).all()
    
    emotion_count = {}  # Diccionario para el recuento de emociones
    
    for stat in statistics:
        emotion = stat.emotion
        if emotion in emotion_count:
            emotion_count[emotion] += 1
        else:
            emotion_count[emotion] = 1
    
    return emotion_count

def calculate_average_age_by_campaign(campaign_id):
    """
    Calcular la edad promedio de los usuarios en una campaña específica.
    :param campaign_id: ID de la campaña.
    :return: Edad promedio.
    """
    statistics = Statistic.query.filter_by(campaign_id=campaign_id).all()
    
    total_age = 0
    user_count = 0
    
    for stat in statistics:
        user = User.query.get(stat.user_id)
        if user and user.age is not None:
            total_age += user.age
            user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        return average_age
    else:
        return None

def calculate_emotion_duration(campaign_id, emotion_to_calculate):
    """
    Calcular la duración total de una emoción específica en una campaña.
    :param campaign_id: ID de la campaña.
    :param emotion_to_calculate: Emoción para calcular la duración.
    :return: Duración total de la emoción en segundos.
    """
    statistics = Statistic.query.filter_by(campaign_id=campaign_id, emotion=emotion_to_calculate).order_by(Statistic.timestamp).all()
    
    total_duration = 0
    start_time = None
    
    for stat in statistics:
        if start_time is not None:
            total_duration += (stat.timestamp - start_time).total_seconds()
            start_time = None
        else:
            start_time = stat.timestamp
    
    return total_duration

def generate_campaign_statistics(campaign_id):
    """
    Generar estadísticas para una campaña específica.
    :param campaign_id: ID de la campaña.
    :return: Diccionario con las estadísticas.
    """
    emotion_count = count_emotions_by_campaign(campaign_id)
    average_age = calculate_average_age_by_campaign(campaign_id)
    emotion_duration = {}
    for emotion in emotion_count.keys():
        duration = calculate_emotion_duration(campaign_id, emotion)
        emotion_duration[emotion] = duration
    
    campaign_statistics = {
        "emotion_count": emotion_count,
        "average_age": average_age,
        "emotion_duration": emotion_duration
    }
    
    return campaign_statistics
