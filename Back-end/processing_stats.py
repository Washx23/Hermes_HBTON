""" Processing stats"""

class Procesamiento:
    def __init__(self, emotions_model):
        self.emotions_model = emotions_model
        self.emotions_data = []

    def process_emotions(self, emotions):
        self.emotions_data.extend(emotions)

    def calculate_statistics(self):
        # Implementa la lógica para calcular estadísticas
        pass

    def save_in_database(self):
        # Implementa la lógica para guardar datos en la base de datos
        pass