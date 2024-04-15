import random
import string

def generate_random_string(longitud, semilla):
    random.seed(semilla)  # Establecer la semilla para reproducir el mismo string
    caracteres = string.ascii_letters + string.digits  # Caracteres posibles
    return ''.join(random.choice(caracteres) for _ in range(longitud))