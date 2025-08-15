import core.config  as estado
from core.timers import avanzar_hora
from core.energy import verificar_energia
from core.animatronics import animatronics
from ui.screens import mapa_interactivo, pantalla_game_over, seleccionar_dificultad, intro
from utils.utils import limpiar_pantalla

from colorama import init, Fore, Style
init(autoreset=True)

from threading import Thread


def juego():
    """
    Inicia la lógica principal del juego, lanzando los hilos necesarios y gestionando el ciclo principal.

    Esta función crea y arranca hilos daemon para:
        - Mover cada animatrónico según su comportamiento.
        - Verificar continuamente el nivel de energía.
        - Avanzar la hora del juego en intervalos definidos.

    Luego entra en un bucle que limpia la pantalla y muestra el mapa interactivo mientras el juego sigue en curso,
    hasta que se activa `stop_event`, indicando que la partida terminó (ya sea por victoria, muerte o salida manual).

    Variables globales:
        Ninguna.

    Notas:
        - Los hilos daemon permiten que se terminen automáticamente al cerrar el programa.
        - El bucle principal se detiene de forma controlada cuando se activa `stop_event`,
          garantizando que todos los hilos en espera se liberen inmediatamente.
        - `stop_event` centraliza ahora la gestión del ciclo de vida de todos los hilos y bucles del juego.
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

        La función solicita al jugador seleccionar la dificultad y luego inicializa 
        las variables globales de estado del juego (`juego_activo`, `hora_actual`, `energia_actual`, 
        `energia_agotada`) y reinicia la posición, velocidad de movimiento y estado de aceleración 
        de cada animatrónico según la dificultad elegida.

        También limpia y reinicia el `stop_event` para permitir que los hilos de la nueva partida 
        se ejecuten correctamente sin interferencias de una partida anterior.

        Luego muestra la introducción narrativa del juego, espera un breve tiempo, reproduce 
        una animación de inicio, y finalmente llama a la función principal `juego()` 
        para lanzar todos los hilos y comenzar la partida.

        Variables globales:
            juego_activo (bool): Indica si el juego está en curso.
            hora_actual (int): Hora inicial del juego.
            energia_actual (int): Nivel inicial de energía del jugador.
            energia_agotada (bool): Bandera que indica si la energía se ha agotado.

        Notas:
            - `stop_event.clear()` se utiliza para reiniciar el control multihilo, 
              permitiendo iniciar una partida nueva sin conflictos con hilos anteriores.
            - `seleccionar_dificultad()` define los parámetros relevantes para la partida actual.
            - La animación de inicio consiste en una serie de puntos impresos con pausas visuales.
            - Llama a `juego()` al final para iniciar la ejecución principal y lanzar los hilos de juego.
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
            anim.ia_level = max(1, anim.ia_level - 4) # Menos agresivo
        elif estado.config["dificultad"] == "DIFICIL":
            anim.ia_level = anim.ia_level # Base
        elif estado.config["dificultad"] == "PESADILLA":
            anim.ia_level = max(20, anim.ia_level + 5) # Mas agresivo

    limpiar_pantalla()    
    juego()


