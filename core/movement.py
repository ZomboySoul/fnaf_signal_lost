from core.animatronics import animatronics
import core.config as estado
from utils.utils import reproducir_sonido


def mover_animatronico(nombre):

    """
        Controla el movimiento de un animatrónico específico durante el juego.

        Esta función ejecuta un bucle que mueve al animatrónico identificado por `nombre` en 
        intervalos definidos por su tiempo de movimiento (`anim.tiempo_movimiento`). 
        El bucle continúa ejecutándose mientras `stop_event` no haya sido activado.

        Cuando el animatrónico llega a la posición 8 (la oficina), se activa la secuencia de muerte:
        se detienen todos los sonidos, se reproduce su canción de muerte, y se muestra la pantalla
        de Game Over. Además, se sincroniza correctamente el acceso a los recursos compartidos 
        mediante locks para evitar condiciones de carrera.

        Args:
            nombre (str): Clave que identifica al animatrónico en el diccionario `animatronics`.

        Locks de threading:
            movimiento_lock (threading.Lock): Asegura la sincronización del movimiento entre hilos.
            muerte_lock (threading.Lock): Sincroniza la rutina de muerte para evitar conflictos.

        Notas:
            - Debe ejecutarse en un hilo separado por cada animatrónico.
            - El bucle se interrumpe de forma controlada cuando se activa `stop_event`, 
              garantizando una detención inmediata de los hilos.
            - El uso de `stop_event.wait(tiempo)` permite que la espera sea interrumpible 
              para finalizar el juego sin demoras.
    """

    anim = animatronics[nombre]

    while not estado.stop_event.wait(anim.tiempo_movimiento):
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
            anim.mover()                   


def detener_todos_los_canales():

    """
        Detiene todos los sonidos en los canales de pasos e interfaz.
    """

    estado.canal_pasos.stop()
    estado.canal_interface.stop()
