import core.config as estado
from utils.utils import limpiar_pantalla
from utils.utils import reproducir_sonido
from core.animatronics import animatronics

from colorama import Fore, init, Style
init(autoreset=True)

import time

def avanzar_hora():

    """
        Avanza la hora del juego en intervalos definidos hasta llegar a la hora límite.

        Esta función ejecuta un bucle que incrementa la variable global `hora_actual` 
        cada cierto tiempo definido en la configuración (`config["tiempo_avanzar_hora"]`). 
        Cada vez que la hora avanza, se ajustan las velocidades de los animatrónicos 
        en caso de ser necesario.

        Cuando la hora llega a 8, se limpia la pantalla, se reproduce el sonido de victoria, 
        se muestra un mensaje de triunfo y se activa `stop_event` para detener todos los hilos activos.

        Args:
            Ninguno.

        Variables globales:
            hora_actual (int): Representa la hora actual del juego.

        Notas:
            - Esta función debe ejecutarse en un hilo separado para no bloquear la ejecución principal.
            - El bucle se interrumpe de forma controlada cuando se activa `stop_event`, 
              garantizando una detención inmediata sin necesidad de esperar a la próxima espera.
            - El uso de `stop_event.wait(tiempo)` permite que la espera entre horas sea interrumpible 
              al instante de finalizar el juego.
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
        Acelera la velocidad de movimiento de todos los animatrónicos a partir de las 4 AM,
        reduciendo su tiempo de desplazamiento en un 60 %, sin permitir que sea menor a 5 segundos.

        Marca a cada animatrónico como acelerado para evitar aplicar la reducción varias veces.

        Args:
            hora_actual (int): Hora actual del juego.
    """

    if hora_actual >= 4:
        for nombre, anim in animatronics.items():
            # Si no está ya acelerado (para no repetir)
            if not anim.acelerado:
                # Reducir tiempo en un 60%
                nuevo_tiempo = int(anim.tiempo_movimiento * 0.6)
                # Evitar que se vuelva 0
                anim.tiempo_movimiento = max(5, nuevo_tiempo)
                # Marcamos que ya se aceleró
                anim.acelerado = True

