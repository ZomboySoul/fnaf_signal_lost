"""
timers.py

Controla la progresión de la hora en el juego y ajusta la velocidad
de los animatrónicos según la hora.
"""

import time
import random

from colorama import Fore, init, Style
init(autoreset=True)

import core.config as estado
from utils.utils import limpiar_pantalla, reproducir_sonido
from core.animatronics import animatronics


def avanzar_hora():
    """
    Avanza la hora del juego en intervalos definidos hasta la hora límite.

    Ejecuta un bucle que incrementa la variable global `hora_actual` 
    cada cierto tiempo definido en la configuración (`config["tiempo_avanzar_hora"]`). 
    Cada vez que la hora avanza, se ajustan las velocidades de los animatrónicos 
    según corresponda.

    Al llegar a la hora 8:
        - Se limpia la pantalla.
        - Se reproduce el sonido de victoria.
        - Se muestra un mensaje de triunfo.
        - Se activa `stop_event` para detener todos los hilos activos.

    Variables globales:
        hora_actual (int): Representa la hora actual del juego.

    Notas:
        - Debe ejecutarse en un hilo separado para no bloquear la ejecución principal.
        - El bucle se interrumpe cuando se activa `stop_event`.
        - `stop_event.wait(tiempo)` permite interrupciones inmediatas de la espera.
    """
    while not estado.stop_event.wait(estado.config["tiempo_avanzar_hora"]):
        if estado.hora_actual < 8:
            estado.hora_actual += 1
            ajustar_tiempos_por_hora(estado.hora_actual)
        if estado.hora_actual == 8:
            limpiar_pantalla()
            reproducir_sonido(estado.config["sonido_victoria"])
            print(Fore.GREEN + Style.BRIGHT + "\n¡6 AM!\n")
            estado.stop_event.set()
            time.sleep(1)
            break


def ajustar_tiempos_por_hora(hora_actual):
    """
    Ajusta la velocidad de movimiento de los animatrónicos según la hora.

    A partir de la hora 6 (6 AM):
        - Reduce el tiempo de desplazamiento de los animatrónicos en un 60 %
          sin permitir que sea menor a 5 segundos.
        - Marca a cada animatrónico como acelerado para evitar aplicar
          la reducción varias veces.

    Args:
        hora_actual (int): Hora actual del juego.
    """
    if hora_actual >= 6:
        for nombre, anim in animatronics.items():
            if not anim.acelerado:
                # Ajusta IA para simular aceleración
                anim.ia_level = max(5, anim.ia_level - random.randint(1, 5))
                anim.acelerado = True
