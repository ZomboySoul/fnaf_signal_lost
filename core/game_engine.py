"""
game_engine.py

Define la lógica principal del juego, gestionando el ciclo de juego,
hilos de animatrónicos, control de energía, avance de hora y pantalla
interactiva.
"""

from colorama import init

# Inicialización de Colorama
init(autoreset=True)

from threading import Thread

import core.config as estado
from core.timers import avanzar_hora
from core.energy import verificar_energia
from core.animatronics import animatronics
from ui.screens import (
    mapa_interactivo,
    pantalla_game_over,
    seleccionar_dificultad,
    intro,
)
from utils.utils import limpiar_pantalla


def juego():
    """
    Inicia la lógica principal del juego y lanza los hilos necesarios.

    Crea y arranca hilos daemon para:
        - Mover cada animatrónico según su comportamiento.
        - Verificar continuamente el nivel de energía.
        - Avanzar la hora del juego en intervalos definidos.
        - Reproducir la introducción narrativa.

    Luego entra en un bucle que limpia la pantalla y muestra el mapa
    interactivo mientras el juego sigue en curso, hasta que se activa
    `stop_event`, indicando que la partida terminó.

    Variables globales:
        Ninguna.

    Notas:
        - Los hilos daemon permiten que se terminen automáticamente al
          cerrar el programa.
        - El bucle principal se detiene de forma controlada cuando se
          activa `stop_event`, liberando los hilos en espera.
        - `stop_event` centraliza la gestión del ciclo de vida de todos
          los hilos y bucles del juego.
    """
    Thread(target=verificar_energia, daemon=True).start()
    Thread(target=avanzar_hora, daemon=True).start()
    Thread(target=intro, daemon=True).start()

    while not estado.stop_event.is_set():
        limpiar_pantalla()
        mapa_interactivo()
        if estado.stop_event.is_set():
            break

    if estado.motivo_game_over:
        pantalla_game_over(estado.motivo_game_over)


def iniciar_juego():
    """
    Configura e inicia una nueva partida del juego.

    Solicita al jugador seleccionar la dificultad y luego inicializa
    las variables de estado del juego (`juego_activo`, `hora_actual`,
    `energia_actual`, `energia_agotada`) y reinicia la posición,
    velocidad de movimiento y estado de aceleración de cada animatrónico.

    También limpia y reinicia `stop_event` para permitir que los hilos
    de la nueva partida se ejecuten correctamente sin interferencias
    de una partida anterior.

    Finalmente, muestra la introducción del juego y llama a `juego()`
    para comenzar la partida principal.

    Variables globales:
        juego_activo (bool): Indica si el juego está en curso.
        hora_actual (int): Hora inicial del juego.
        energia_actual (int): Nivel inicial de energía del jugador.
        energia_agotada (bool): Bandera que indica si la energía se ha
                                agotado.

    Notas:
        - `stop_event.clear()` reinicia el control multihilo para evitar
          conflictos con hilos anteriores.
        - `seleccionar_dificultad()` define los parámetros para la partida
          actual.
        - La animación de inicio consiste en puntos impresos con pausas.
        - `juego()` lanza los hilos principales y gestiona el ciclo de juego.
    """
    seleccionar_dificultad()
    estado.stop_event.clear()

    estado.juego_activo = True
    estado.hora_actual = 0
    estado.energia_actual = 100
    estado.energia_agotada = False

    for nombre, anim in animatronics.items():
        anim.posicion = anim.spawn
        anim.acelerado = False

        if estado.config["dificultad"] == "NORMAL":
            anim.ia_level = max(1, anim.ia_level - 4)
        elif estado.config["dificultad"] == "DIFICIL":
            anim.ia_level = anim.ia_level
        elif estado.config["dificultad"] == "PESADILLA":
            anim.ia_level = max(20, anim.ia_level + 5)

    limpiar_pantalla()
    juego()
