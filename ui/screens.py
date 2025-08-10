from utils.utils import limpiar_pantalla
from core.energy import barra_energia
import core.config as estado
from core.animatronics import animatronics
from utils.utils import reproducir_sonido, cargar_plantilla_archivo
from core.movement import detener_todos_los_canales, mover_animatronico

from colorama import Fore, init, Style
init(autoreset=True)

from threading import Thread

import msvcrt
import time

import pygame
pygame.init()


def mostrar_mapa(camara_seleccionada):

    """
        Muestra en pantalla el mapa de cámaras interactivo, resaltando la cámara seleccionada.

        Args:
            camara_seleccionada (int): Número de cámara actualmente seleccionada.
    """

    limpiar_pantalla()
    def cam_texto(numero):
        texto = f"CAM 0{numero}"
        if camara_seleccionada == numero:
            return Fore.RED + texto + Style.RESET_ALL
        else:
            return texto

    print("\r" + barra_energia(), end="", flush=True)
    print(Fore.LIGHTYELLOW_EX + f"\nHora: {estado.horas[estado.hora_actual]}\n")    
    print(Fore.LIGHTWHITE_EX + f"""
                      ╔══════════╗
               ╔══════╣  {cam_texto(2)}  ╠════════════╗
               ║      ╚══════════╝            ║
             ╔═╩══════╗                 ╔═════╩══╗
      ╔══════╣        ║  ╔════════════╗ ║        ║
   ╔══╩═════╗║ {cam_texto(6)} ╠══╣   {cam_texto(1)}   ╠═╣ {cam_texto(3)} ╠══╗
   ║        ║║        ║  ╚════════╦═══╝ ║        ║  ║
   ║ {cam_texto(7)} ║╚══╦═════╝           ║     ╚═╦═══╦══╝  ║
   ║        ║   ║     ╔════════╗  ║       ║   ║     ║
   ╚══╦═════╝   ╚═════╣ {cam_texto(5)} ╠══╩═══════╝   ║     ║
      ║               ╚════════╝              ╠═════╝
      ║           ╔═════════════════╗         ║  
      ╚═══════════╣	 {cam_texto(4)}     ╠═════════╝   
                  ╚════╦══════╦═════╝        
                    ╔══╝      ╚══╗
                    ║   ╔════╗   ║        
                    ╚═══╣ CG ╠═══╝
                        ╚════╝
    """)

    print(f"\nCámara seleccionada: {camara_seleccionada}")
    print("Q pasa salir")


def mapa_interactivo():

    """
        Muestra un mapa interactivo de las cámaras de seguridad, permitiendo al jugador
        navegar entre ellas usando las flechas del teclado y seleccionarlas con Enter.
    
        Controles:
            - Flechas arriba/derecha: avanza a la siguiente cámara disponible.
            - Flechas abajo/izquierda: retrocede a la cámara anterior.
            - Enter: muestra la habitación seleccionada si hay batería disponible.
            - Q: sale del juego y finaliza la partida.
    
        Controla además el refresco automático de la pantalla cada segundo para actualizar
        la visualización de batería y hora.
    
        El bucle principal se mantiene activo hasta que se activa `stop_event`, indicando 
        que la partida terminó por Game Over, victoria o salida manual, garantizando una
        detención controlada de la interfaz.
    
        Variables globales:
            energia_actual (int): Nivel actual de batería del jugador.
    
        Notas:
            - `stop_event.is_set()` se verifica constantemente para permitir la interrupción 
              inmediata del bucle ante cualquier condición de fin de partida.
            - El control multihilo queda sincronizado gracias a `stop_event`, unificando 
              la gestión de cierre de todos los hilos y bucles activos del juego.
    """


    camaras_disponibles = [1, 2, 3, 4, 5, 6, 7]
    indice = 0
    camara_seleccionada = camaras_disponibles[indice]
    ultimo_refresco = time.time()

    #mostrar mapa
    mostrar_mapa(camara_seleccionada)

    while not estado.stop_event.is_set():
        if time.time() - ultimo_refresco >= estado.config["tiempo_avanzar_hora"]:
            mostrar_mapa(camara_seleccionada)
            ultimo_refresco = time.time()

        if msvcrt.kbhit():
            if estado.stop_event.is_set():
                break

            tecla = msvcrt.getch()
            if tecla == b'\xe0':
                flecha = msvcrt.getch()
                if flecha in [b'H', b'M']:
                    indice = (indice + 1) % len(camaras_disponibles)
                elif flecha in [b'P', b'K']:
                    indice = (indice - 1) % len(camaras_disponibles)
                camara_seleccionada = camaras_disponibles[indice]
                mostrar_mapa(camara_seleccionada)

            elif tecla == b'\r':
                if estado.energia_actual <= 0:
                    print(Fore.RED + "\n¡Sin batería! No podés usar cámaras.")
                    estado.energia_actual = 0
                    time.sleep(1.5)
                else:
                    mostrar_habitacion(camara_seleccionada)
                    if not estado.stop_event.is_set():
                        mostrar_mapa(camara_seleccionada)

                if estado.stop_event.is_set():
                    break

            elif tecla in [b'q', b'Q']:
                estado.stop_event.set()
                print("Saliendo del juego...")
                time.sleep(2)
                detener_todos_los_canales()
                limpiar_pantalla()
                break


def mostrar_habitacion(numero):

    """
        Muestra la visualización de una cámara específica del juego, incluyendo su plantilla gráfica
        y los animatrónicos presentes en esa habitación.
    
        Controla además:
            - Consumo de batería al ingresar a la cámara.
            - Reproducción de sonido de cámara.
            - Detección de animatrónicos presentes y si ocupan su spawn original.
            - Interacción del jugador para usar la linterna o salir.
            - Mensajes contextuales si no queda batería o si el juego ha finalizado.
    
        El flujo de esta función puede interrumpirse en cualquier momento si se activa `stop_event`,
        lo que garantiza una salida inmediata y controlada durante una partida terminada 
        (ya sea por Game Over, victoria o salida manual).
    
        Args:
            numero (int): Número de la cámara a mostrar.
    
        Variables globales:
            energia_actual (int): Nivel actual de batería del jugador.
    
        Notas:
            - Antes de cada interacción y tras cada espera, se verifica `stop_event.is_set()` 
              para cortar la ejecución de la función en caso de ser necesario.
            - La interacción con la linterna permite devolver animatrónicos a su spawn, salvo al dueño
              de la habitación si está presente.
    """
    

    if estado.energia_actual <= 0:
        print(Fore.RED + "¡Sin batería! No podés usar cámaras.")
        time.sleep(2)
        return
    
    estado.energia_actual -= estado.config["energia_uso_camara"]
    estado.energia_actual = max(0, estado.energia_actual)

    if estado.energia_actual <= 0:
        print(Fore.RED + "¡Sin batería! No podés usar cámaras.")
        time.sleep(2)
        return
    
    reproducir_sonido(estado.config["sonido_camara"], canal=estado.canal_interface)
    limpiar_pantalla()
    print(Fore.CYAN + f"[ Cámara {numero:02d} - {estado.habitaciones[numero]} ]\n")

    # Obtener animatrónicos presentes en la cámara
    anim_presentes = [nombre for nombre, anim in animatronics.items() if anim.posicion == numero]

    # Cargar y mostrar plantilla desde archivo
    plantilla = cargar_plantilla_archivo(numero, anim_presentes)
    for linea in plantilla:
        print(Fore.WHITE + linea.rstrip("\n"))

    # Resto de tu código de interacción con linterna etc. abajo sin cambios
    spawn_owners = [nombre for nombre, anim in animatronics.items() if anim.spawn == numero]

    anim_own = any(owner in anim_presentes for owner in spawn_owners)
    todos_son_duenios = all(anim in spawn_owners for anim in anim_presentes)

    if not todos_son_duenios and anim_own:
        if estado.stop_event.is_set():
            return
        print(Fore.YELLOW + "\n¡Animatrónico detectado! Presiona 'F' para usar la linterna.")
        eleccion = input("\n> ").strip().upper()
        if estado.stop_event.is_set():
            return
        if eleccion == 'F':
            usar_linterna(anim_presentes, spawn_owners[0])

    elif todos_son_duenios and anim_presentes:
        if estado.stop_event.is_set():
            return
        print(Fore.RED + "\n¡Linterna Desactivada!")
        input("\nPresiona Enter para volver.")
        if estado.stop_event.is_set():
            return

    elif not anim_own and anim_presentes:
        if estado.stop_event.is_set():
            return
        print(Fore.YELLOW + "\n¡Animatrónico detectado! Presiona 'F' para usar la linterna.")
        eleccion = input("\n> ").strip().upper()
        if estado.stop_event.is_set():
            return
        if eleccion == 'F':
            usar_linterna(anim_presentes, None)

    else:
        if estado.stop_event.is_set():
            return
        if estado.energia_actual <= 0:
            print(Fore.RED + "\nSin batería. No podés seguir usando las cámaras.")
            time.sleep(2)
            return
        else:
            print(Fore.CYAN + "\nPresiona Enter para volver.")
            input()


def usar_linterna(anim_presentes, spawn_owner=None):

    """
        Simula el uso de la linterna en una habitación, permitiendo al jugador hacer retroceder
        a los animatrónicos presentes que no sean dueños del spawn de esa habitación.

        Controla además:
            - Consumo de batería al usar la linterna.
            - Impide su uso si no queda batería.
            - Muestra mensajes de acción por cada animatrónico afectado.

        Args:
            anim_presentes (list): Lista de nombres de animatrónicos presentes en la habitación.
            spawn_owner (str, opcional): Nombre del animatrónico dueño del spawn en esa habitación. No será afectado.

        Variables globales:
            energia_actual (int): Nivel actual de batería del jugador.
    """

    if estado.energia_actual <= 0:
        print(Fore.RED + "¡Sin batería! La linterna no funciona.")
        estado.energia_actual = 0
        time.sleep(1)
        return

    estado.energia_actual -= estado.config["energia_uso_linterna"]
    estado.energia_actual = max(0, estado.energia_actual)

    print(Fore.GREEN + "¡Usaste la linterna!")
    for nombre in anim_presentes:
        if nombre != spawn_owner:
            animatronics[nombre].regresar_spawn()
            print(Fore.GREEN + f"{animatronics[nombre].cara} {nombre} regresó a su posición inicial.")
    time.sleep(1)


def pantalla_game_over(nombre):

    """
        Muestra la pantalla de Game Over cuando un animatrónico entra a la oficina.

        Esta función detiene todos los sonidos activos, activa `stop_event` para detener 
        inmediatamente todos los hilos de juego en ejecución, y reproduce una secuencia de sonidos: 
        powerdown, canción de muerte del animatrónico responsable y jumpscare. 

        Luego muestra en pantalla un mensaje visual con un banner estilizado que indica qué 
        animatrónico causó el Game Over.

        Después de una breve pausa, informa que se volverá al menú principal y llama a `menu_principal()` 
        para reiniciar el flujo del juego.

        Args:
            nombre (str): Clave que identifica al animatrónico responsable dentro del diccionario `animatronics`.

        Variables globales:
            juego_activo (bool): Indica si el juego está en curso.

        Notas:
            - La función usa `pygame.mixer.music` y canales de sonido para controlar la reproducción de audio,
              esperando a que finalicen antes de continuar.
            - Activa `stop_event` para detener de forma inmediata todos los hilos que supervisan animatrónicos, 
              avance de hora y consumo de energía.
            - Imprime en consola un mensaje de Game Over con colores y ASCII art.
            - Tras mostrar el mensaje, vuelve al menú principal del juego.
    """


    animatronic = animatronics[nombre]
    detener_todos_los_canales()
    
    
    reproducir_sonido(estado.config["sonido_powerdown"])
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    reproducir_sonido(animatronic.cancion_muerte)
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    reproducir_sonido(estado.config["sonido_jumpscare"])
    time.sleep(1.5)
    

    estado.stop_event.set() 
    estado.juego_activo = False
    
    limpiar_pantalla()
    ancho_pantalla = 80
    print()
    mensaje = [
        Fore.RED + Style.BRIGHT + f"¡{nombre.upper()} ENTRÓ A LA OFICINA!".center(ancho_pantalla),
        "",
        Fore.MAGENTA + Style.BRIGHT + "  ██████╗   █████╗  ███╗   ███╗ ███████╗     ██████╗  ██╗   ██╗ ███████╗ ██████╗ ",
        Fore.MAGENTA + Style.BRIGHT + " ██╔════╝  ██╔══██╗ ████╗ ████║ ██╔════╝    ██╔═══██╗ ██║   ██║ ██╔════╝ ██╔══██╗",
        Fore.MAGENTA + Style.BRIGHT + " ██║  ███╗ ███████║ ██╔████╔██║ █████╗      ██║   ██║ ██║   ██║ █████╗   ██████╔╝",
        Fore.MAGENTA + Style.BRIGHT + " ██║   ██║ ██╔══██║ ██║╚██╔╝██║ ██╔══╝      ██║   ██║ ███╗ ███║ ██╔══╝   ██╔══██╗",
        Fore.MAGENTA + Style.BRIGHT + " ╚██████╔╝ ██║  ██║ ██║ ╚═╝ ██║ ███████╗    ╚██████╔╝ ╚═████╔═╝ ███████╗ ██║  ██║",
        Fore.MAGENTA + Style.BRIGHT + "  ╚═════╝  ╚═╝  ╚═╝ ╚═╝     ╚═╝ ╚══════╝     ╚═════╝    ╚═══╝   ╚══════╝ ╚═╝  ╚═╝"
    ]

    for linea in mensaje:
        print(linea)
        time.sleep(0.3)

    time.sleep(2)
    print(Fore.YELLOW + "volviendo al menú principal...".center(ancho_pantalla))
    time.sleep(1)
    from ui.menu import menu_principal
    menu_principal()


def mostrar_historia():

    """
        Muestra la introducción narrativa del juego, relatando los hechos previos a la partida
        con una animación de texto caracter por caracter en pantalla.

        Describe el contexto de Freddy's Family Diner, las desapariciones ocurridas
        y la misión del jugador como vigilante nocturno.

        No recibe argumentos ni retorna valores.
    """

    limpiar_pantalla()
    texto = [
        ("Corría el año 1987. Un pequeño restaurante familiar llamado"),
        ("'Freddy's Family Diner' abría sus puertas al público."),
        ("Todo era diversión... hasta que empezaron las desapariciones."),
        ("Los rumores dicen que los animatrónicos tienen voluntad propia,"),
        ("y durante la noche, rondan el local buscando presas."),
        ("Como nuevo vigilante nocturno, tu misión es sobrevivir"),
        ("vigilando las cámaras y usando tu linterna."),
        ("Pero cuidado... no todos los secretos han sido revelados."),
        ("¿Podrás sobrevivir hasta las 6 AM?\n")
    ]
    for linea in texto:
        for caracter in linea:
            print(caracter, end="", flush=True)
            time.sleep(0.03)
        print()  # Salto de línea
        time.sleep(0.5)


def intro():
    """
    Reproudce una inroduccion de audio mientras el jugador puede interactuar,
    pero los animatronicos no se mueven hasta que el audio termine
    """

    reproducir_sonido(estado.config["intro"])

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Cuando termina el audio, iniciar el hilo de movimiento
    for nombre in animatronics:
        Thread(target=mover_animatronico, args=(nombre,), daemon=True).start()

def mostrar_instrucciones():
    
    """
        Muestra en pantalla las instrucciones del juego, explicando controles, objetivos,
        mecánicas básicas, uso de cámaras y linterna, y las condiciones de victoria o derrota.

        Presenta también la duración de cada dificultad disponible.

        Espera a que el jugador presione una tecla para volver al menú principal.

        No recibe argumentos ni retorna valores.
    """
    
    limpiar_pantalla()

    print()
    print("════════════════════════════════════════")
    print(Style.BRIGHT + Fore.MAGENTA + "📜 INSTRUCCIONES 📜".center(38))
    print("════════════════════════════════════════")
    print("")

    print(Style.BRIGHT + Fore.WHITE + "- Usa las flechas " + Fore.CYAN + "↑ ↓ ← →" + Fore.WHITE + " para moverte por el mapa.\n")    
    print(Fore.WHITE + "- Tu objetivo es " + Fore.RED + "sobrevivir la noche" + Fore.WHITE + " vigilando las cámaras.\n")
    print(Fore.WHITE + "- Observa los movimientos de los animatrónicos.\n")
    print(Fore.WHITE + "- Usa la " + Fore.LIGHTYELLOW_EX + "linterna" + Fore.WHITE + " para espantarlos.\n")
    print(Fore.WHITE + "- Si un animatrónico entra en la oficina... " + Fore.RED + Style.BRIGHT + "¡será tu fin!\n")
    print(Fore.WHITE + "- La noche dura un tiempo según el modo de dificultad:")
    print(Fore.LIGHTGREEN_EX + "  • NORMAL: 8 minutos\n" +
          Fore.LIGHTYELLOW_EX + "  • DIFICIL: 16 minutos\n" +
          Fore.LIGHTMAGENTA_EX + "  • PESADILLA: 30 minutos\n" + 
          Fore.WHITE + "  Intenta sobrevivir todo el tiempo... " + Fore.RED + "¡si puedes!\n")
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX + "\nPresiona cualquier tecla para volver al menú...")

    msvcrt.getch()


def seleccionar_dificultad():

    """
        Muestra un menú interactivo de selección de dificultad para el juego, permitiendo
        al jugador elegir entre NORMAL, DIFÍCIL, PESADILLA o VOLVER al menú principal.

        Cada dificultad modifica:
            - Velocidad de avance de las horas.
            - Consumo de energía por linterna.
            - Consumo de energía por uso de cámara.

        Controles:
            - Flechas arriba/abajo: navegan entre las opciones.
            - Enter: confirma la selección.

        Variables globales:
            config (dict): Diccionario que contiene los parámetros de configuración del juego.
    """

    opciones = ["NORMAL", "DIFÍCIL", "PESADILLA", "VOLVER"]
    ancho_pantalla = 60
    seleccion = 0

    while True:
        limpiar_pantalla()

        print(Style.BRIGHT + Fore.WHITE + """
                    
        ███╗   ███╗  ██████╗  ██████╗   ██████╗  ███████╗
        ████╗ ████║ ██╔═══██╗ ██╔══██╗ ██╔═══██╗ ██╔════╝
        ██╔████╔██║ ██║   ██║ ██║  ██║ ██║   ██║ ███████╗
        ██║╚██╔╝██║ ██║   ██║ ██║  ██║ ██║   ██║ ╚════██║
        ██║ ╚═╝ ██║ ╚██████╔╝ ██████╔╝ ╚██████╔╝ ███████║
        ╚═╝     ╚═╝  ╚═════╝  ╚═════╝   ╚═════╝  ╚══════╝
        """)


        for i, opcion in enumerate(opciones):
            flecha = ">> " if i == seleccion else "   "
            
            if i == 0:
                color = Fore.GREEN
            elif i == 1:
                color = Fore.YELLOW
            elif i == 2:
                color = Fore.MAGENTA
            else:
                color = Fore.WHITE

            linea = flecha + opcion
            print("\n" + color + linea.center(ancho_pantalla))

        tecla = msvcrt.getch()

        if tecla == b'\xe0':
            flecha = msvcrt.getch()
            if flecha == b'H':
                seleccion = (seleccion - 1) % len(opciones)
            elif flecha == b'P':
                seleccion = (seleccion + 1) % len(opciones)

        elif tecla == b'\r':
            if seleccion == 0:
                estado.config["tiempo_avanzar_hora"] = 60
                estado.config["energia_uso_linterna"] = 5
                estado.config["energia_uso_camara"] = 2
                estado.config["dificultad"] = "NORMAL"
            elif seleccion == 1:
                estado.config["tiempo_avanzar_hora"] = 120
                estado.config["energia_uso_linterna"] = 3
                estado.config["energia_uso_camara"] = 1.5
                estado.config["dificultad"] = "DIFICIL"
            elif seleccion == 2:
                estado.config["tiempo_avanzar_hora"] = 225
                estado.config["energia_uso_linterna"] = 2
                estado.config["energia_uso_camara"] = 1
                estado.config["dificultad"] = "PESADILLA"
            elif seleccion == 3:
                from main import menu_principal
                menu_principal()
            time.sleep(1)
            return
