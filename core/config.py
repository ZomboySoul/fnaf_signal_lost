"""
config.py

Configuración global del juego FNAF en consola.

Define variables de estado, rutas de archivos, sonidos, locks y horarios
de las habitaciones. También inicializa pygame y canales de audio.
"""

import os
import warnings
from threading import Event, Lock


# Ignorar warnings de Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=UserWarning)

# Inicialización de Pygame
import pygame
pygame.init()

# Evento global para detener threads
stop_event = Event()

# Ruta base absoluta del proyecto (carpeta raíz)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Estado del juego
hora_actual = 0
energia_actual = 100
energia_agotada = False
juego_activo = False
motivo_game_over = None

# Configuración general
config = {
    # Energía y tiempos
    "energia_uso_linterna": 0,
    "energia_uso_camara": 0,
    "tiempo_avanzar_hora": 0,
    "dificulta": "",

    # Rutas de carpetas
    "carpeta_sonidos": os.path.join(BASE_DIR, "sound"),
    "carpeta_rooms": os.path.join(BASE_DIR, "rooms"),

    # Sonidos globales
    "sonido_powerdown": "powerdown.mp3",
    "sonido_victoria": "victoria_time.mp3",
    "sonido_jumpscare": "jumpscare.mp3",
    "sonido_camara": "camara_sound.mp3",
    "intro": "intro.wav",
}

# Locks globales para sincronización de threads
movimiento_lock = Lock()
muerte_lock = Lock()

# Horario de turno
horas = [
    "10 AM", "11 AM", "12 AM", "01 AM", "02 AM", 
    "03 AM", "04 AM", "05 AM", "06 AM"
]

# Habitaciones del mapa
habitaciones = {
    1: "Comedor",
    2: "Escenario",
    3: "Baños",
    4: "Cocina",
    5: "Pasillo Central",
    6: "Bastidores",
    7: "Cueva del Pirata",
    8: "Oficina"
}

# Canales de audio
canal_interface = pygame.mixer.Channel(1)
canal_pasos_freddy = pygame.mixer.Channel(2)
canal_pasos_bonnie = pygame.mixer.Channel(3)
canal_pasos_chica = pygame.mixer.Channel(4)
canal_pasos_foxy = pygame.mixer.Channel(5)
