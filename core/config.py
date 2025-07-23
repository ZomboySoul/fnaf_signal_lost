from threading import Lock

from threading import Event
stop_event = Event()

import pygame
pygame.init()

import os

# Ruta base absoluta del proyecto (carpeta raíz)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))


hora_actual = 0 

energia_actual = 100
energia_agotada = False

juego_activo = False
motivo_game_over = None 

config = {
    # Energía y tiempos
    "energia_uso_linterna": 0,
    "energia_uso_camara": 0,
    "tiempo_avanzar_hora": 0,

    # Rutas de carpetas
    "carpeta_sonidos": os.path.join(BASE_DIR, "sound"),
    "carpeta_rooms": os.path.join(BASE_DIR, "rooms"),

    # Sonidos globales
    "sonido_powerdown": "powerdown.mp3",
    "sonido_victoria": "victoria_time.mp3",
    "sonido_jumpscare": "jumpscare.mp3",
    "sonido_camara": "camara_sound.mp3",

    # Parámetros de AI
    "tiempo_movimiento_freddy": 45,
    "tiempo_movimiento_foxy": 15,
    "tiempo_movimiento_chica": 12,
    "tiempo_movimiento_bonnie": 13
}

# LOCKS
movimiento_lock = Lock()
muerte_lock = Lock()


# HORARIO DE TURNO
horas = ["10 AM", "11 AM", "12 AM", "01 AM", "02 AM", "03 AM", "04 AM", "05 AM", "06 AM"]


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

canal_pasos = pygame.mixer.Channel(1)
canal_interface = pygame.mixer.Channel(2)
