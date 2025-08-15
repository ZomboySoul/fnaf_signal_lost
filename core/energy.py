"""
energy.py

Funciones para supervisar y representar el nivel de energía del jugador
durante el juego. Incluye verificación de energía y barra gráfica.
"""

from colorama import Fore, init
import core.config as estado

# Inicialización de Colorama
init(autoreset=True)


def verificar_energia():
    """
    Supervisa el nivel de energía del jugador durante el juego.

    Ejecuta un bucle que verifica, cada segundo, si la energía actual
    se ha agotado. Si llega a cero y aún no se había detectado, marca
    la energía como agotada y detiene el juego indicando a "Freddy"
    como responsable.

    Se espera que esta función se ejecute en un hilo separado.

    Notas:
        - El bucle se detiene automáticamente cuando se activa `stop_event`.
        - El uso de `stop_event.wait(1)` permite interrupciones inmediatas
          del hilo, evitando esperas innecesarias.

    Variables globales:
        energia_actual (int): Nivel actual de energía del jugador.
        energia_agotada (bool): Indica si ya se detectó energía agotada.
        motivo_game_over (str): Motivo por el que terminó el juego.
    """
    while not estado.stop_event.wait(1):
        if estado.energia_actual <= 0 and not estado.energia_agotada:
            estado.energia_agotada = True
            estado.motivo_game_over = "Freddy"
            estado.stop_event.set()


def barra_energia():
    """
    Genera y devuelve una representación gráfica de la barra de energía.

    Returns:
        str: Texto formateado con la barra de energía y porcentaje actual.
    """
    energia = estado.energia_actual

    if energia >= 90:
        bloques = 8
    elif energia >= 75:
        bloques = 7
    elif energia >= 62:
        bloques = 6
    elif energia >= 50:
        bloques = 5
    elif energia >= 35:
        bloques = 4
    elif energia >= 20:
        bloques = 3
    elif energia >= 12:
        bloques = 2
    elif energia >= 5:
        bloques = 1
    else:
        bloques = 0

    barra = "█" * bloques + " " * (8 - bloques)

    if energia <= 0:
        return Fore.RED + f"[{barra}] " + Fore.RED + "SIN ENERGÍA"
    elif energia <= 4:
        return Fore.RED + f"[{barra}] " + Fore.RED + f"{energia}%"
    elif energia <= 12:
        return Fore.YELLOW + f"[{barra}] " + Fore.YELLOW + f"{energia}%"
    elif energia <= 35:
        return Fore.LIGHTYELLOW_EX + f"[{barra}] " + Fore.LIGHTYELLOW_EX + f"{energia}%"
    else:
        return Fore.GREEN + f"[{barra}] " + Fore.GREEN + f"{energia:.0f}%"
