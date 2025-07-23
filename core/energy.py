import core.config as estado
from colorama import Fore, init
init(autoreset=True)


def verificar_energia():

    """
        Supervisa continuamente el nivel de energía durante el juego.

        Esta función ejecuta un bucle que verifica, cada segundo, si la energía actual se ha agotado.
        Si la energía llega a cero y aún no se había detectado, marca la energía como agotada 
        y muestra la pantalla de Game Over indicando a "Freddy" como responsable.

        El bucle se detiene automáticamente cuando se activa `stop_event`, permitiendo finalizar 
        de forma controlada desde otras partes del juego sin depender de banderas booleanas.

        Args:
            Ninguno.

        Variables globales:
            energia_actual (int): Nivel actual de energía del jugador.
            energia_agotada (bool): Bandera que indica si ya se detectó la energía agotada.

        Notas:
            - Se espera que esta función se ejecute en un hilo separado.
            - El uso de `stop_event.wait(1)` permite que la espera sea interrumpible 
              al instante en que se detiene el juego, evitando esperas innecesarias.
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
        return Fore.LIGHTGREEN_EX + f"[{barra}] " + Fore.RED + "SIN ENERGÍA"    
    elif energia <= 4:
        return Fore.LIGHTGREEN_EX + f"[{barra}] " + Fore.RED + f"{energia}%"
    elif energia <= 12:
        return Fore.LIGHTGREEN_EX + f"[{barra}] " + Fore.YELLOW + f"{energia}%"
    elif energia <= 35:
        return Fore.LIGHTGREEN_EX + f"[{barra}] " + Fore.LIGHTYELLOW_EX + f"{energia}%"
    else:
        return Fore.LIGHTGREEN_EX + f"[{barra}] " + Fore.GREEN + f"{energia:.0f}%"
