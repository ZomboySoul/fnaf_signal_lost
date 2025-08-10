from core.animatronics import animatronics
import core.config as estado
from utils.utils import reproducir_sonido

import random 

def mover_animatronico(nombre):

    """
    Ejecuta el movimiento de un animatrónico en un hilo independiente.

    El animatrónico identificado por `nombre` se mueve en intervalos aleatorios
    definidos por sus atributos `intervalo_min` y `intervalo_max`, y decide moverse
    según su nivel de IA (`ia_level`).

    Si llega a la posición 8 (oficina), se detiene el juego: se reproducen sonidos
    de muerte y se activa el estado de Game Over, asegurando la sincronización
    entre hilos mediante `movimiento_lock` y `muerte_lock`.

    Args:
        nombre (str): Nombre clave del animatrónico en el diccionario `animatronics`.

    Notas:
        - Usar en un hilo separado por animatrónico.
        - `stop_event.wait(tiempo)` permite interrumpir la espera al finalizar el juego.
    """

    anim = animatronics[nombre]

    while not estado.stop_event.is_set():
        # Espera Aleatoria dependiendo del valor del animatronico 
        tiempo_espera = random.uniform(anim.intervalo_min, anim.intervalo_max)
        if estado.stop_event.wait(tiempo_espera):
            break

        with estado.movimiento_lock:
            if anim.posicion == 8:
                with estado.muerte_lock:
                    if estado.stop_event.is_set():
                        break
                    detener_todos_los_canales()
                    reproducir_sonido(anim.cancion_muerte)
                    estado.motivo_game_over = nombre           
                    estado.stop_event.set()
                break
            
            # Freddy no intenta moverse antes de las 3 AM
            if anim.nombre == "Freddy" and estado.hora_actual < 3:
                continue
            
            # IA decide si mueve
            if random.randint(1, 20) <= anim.ia_level:
                anim.mover()                   


def detener_todos_los_canales():

    """
        Detiene todos los sonidos en los canales de pasos e interfaz.
    """

    estado.canal_pasos_chica.stop()
    estado.canal_pasos_bonnie.stop()
    estado.canal_pasos_foxy.stop()
    estado.canal_pasos_freddy.stop()
    estado.canal_interface.stop()
