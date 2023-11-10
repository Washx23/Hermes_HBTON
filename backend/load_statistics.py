import json
from collections import Counter

# Definir el diccionario de emociones
emotions = {0: "angry", 1: "disgust", 2: "fear", 3: "happy", 4: "neutral", 5: "sad", 6: "surprice"}

# Cargar los datos desde un archivo JSON
with open('emotion_results.json', 'r') as f:
    data = json.load(f)

# Contar la frecuencia de cada elemento en los datos
counter = Counter(data)
resultados = []

# Calcular el promedio para cada emoción
for emotion_id, count in counter.items():
    emotion = emotions[emotion_id]
    average = count / len(data)
    print(f'El promedio de {emotion} es: {average:.2f}')
    resultados.append(f'El promedio de {emotion} es: {average:.2f}')

data = "Aquí van tus datos"

# Guardar los datos en un archivo .txt
with open('resultados.txt', 'w') as f:
    f.write('\n'.join(resultados))
