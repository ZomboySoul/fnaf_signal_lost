"""
ui/screens.py

Interfaz visual del juego.

Incluye:
- Mapa interactivo de cámaras.
- Visualización de habitaciones y linterna.
- Pantallas de Game Over, historia, introducción e instrucciones.
- Selección de dificultad.
"""


import os
import time
import msvcrt
import warnings
from threading import Thread

from colorama import Fore, init, Style

from utils.utils import limpiar_pantalla, reproducir_sonido, cargar_plantilla_archivo
from core.energy import barra_energia
import core.config as estado
from core.animatronics import animatronics
from core.movement import mover_animatronico, detener_todos_los_canales

init(autoreset=True)

# Ignorar warnings de Pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=UserWarning)

import pygame
pygame.init()


# -------------------------- MAPA Y CÁMARAS -------------------------- #
def mostrar_mapa(camara_seleccionada):
    """
    Muestra en pantalla el mapa de cámaras interactivo, resaltando la cámara seleccionada.
    
    Args:
        camara_seleccionada (int): Número de cámara actualmente seleccionada.
    """
    limpiar_pantalla()
    def cam_texto(numero):
        texto = f"CAM 0{numero}"
        return Fore.RED + texto + Style.RESET_ALL if camara_seleccionada == numero else texto

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
    print("Presiona 'Q' para salir")


def mapa_interactivo():
    """
    Muestra el mapa interactivo de cámaras y permite navegación.
    Controla refresco de pantalla, batería y sincronización con stop_event.
    """
    camaras_disponibles = [1, 2, 3, 4, 5, 6, 7]
    indice = 0
    camara_seleccionada = camaras_disponibles[indice]
    ultimo_refresco = time.time()

    mostrar_mapa(camara_seleccionada)

    while not estado.stop_event.is_set():
        # Refresco automático
        if time.time() - ultimo_refresco >= estado.config["tiempo_avanzar_hora"]:
            mostrar_mapa(camara_seleccionada)
            ultimo_refresco = time.time()

        # Entrada de usuario
        if msvcrt.kbhit():
            if estado.stop_event.is_set():
                break 
            tecla = msvcrt.getch()
            
            if tecla == b'\xe0':
                flecha = msvcrt.getch()
                if flecha in [b'H', b'M']:  # Arriba/derecha
                    indice = (indice + 1) % len(camaras_disponibles)
                elif flecha in [b'P', b'K']:  # Abajo/izquierda
                    indice = (indice - 1) % len(camaras_disponibles)
                camara_seleccionada = camaras_disponibles[indice]
                mostrar_mapa(camara_seleccionada)

            elif tecla == b'\r':  # Enter
                if estado.energia_actual <= 0:
                    print(Fore.RED + "\n¡Sin batería! No podés usar cámaras.")
                    estado.energia_actual = 0
                    time.sleep(1.5)
                else:
                    mostrar_habitacion(camara_seleccionada)
                    mostrar_mapa(camara_seleccionada)

            elif tecla in [b'q', b'Q']:
                estado.stop_event.set()
                print("Saliendo del juego...")
                time.sleep(2)
                detener_todos_los_canales()
                limpiar_pantalla()
                break


def mostrar_habitacion(numero: int):
    """
    Muestra la cámara seleccionada y permite interacción con linterna.

    Args:
        numero (int): Número de la cámara.
    """
    if estado.energia_actual <= 0:
        print(Fore.RED + "¡Sin batería! No podés usar cámaras.")
        time.sleep(2)
        return

    estado.energia_actual -= estado.config["energia_uso_camara"]
    estado.energia_actual = max(0, estado.energia_actual)

    reproducir_sonido(estado.config["sonido_camara"], canal=estado.canal_interface)
    limpiar_pantalla()
    print(Fore.CYAN + f"[ Cámara {numero:02d} - {estado.habitaciones[numero]} ]\n")

    anim_presentes = [n for n, a in animatronics.items() if a.posicion == numero]
    plantilla = cargar_plantilla_archivo(numero, anim_presentes)
    for linea in plantilla:
        print(Fore.WHITE + linea.rstrip("\n"))

    spawn_owners = [n for n, a in animatronics.items() if a.spawn == numero]
    anim_own = any(owner in anim_presentes for owner in spawn_owners)
    todos_son_duenios = all(anim in spawn_owners for anim in anim_presentes)

    if not todos_son_duenios and anim_own:
        print(Fore.YELLOW + "\n¡Animatrónico detectado! Presiona 'F' para usar la linterna.")
        if input("\n> ").strip().upper() == 'F':
            usar_linterna(anim_presentes, spawn_owners[0])
    elif todos_son_duenios and anim_presentes:
        print(Fore.RED + "\n¡Linterna Desactivada!")
        input("\nPresiona Enter para volver.")
    elif not anim_own and anim_presentes:
        print(Fore.YELLOW + "\n¡Animatrónico detectado! Presiona 'F' para usar la linterna.")
        if input("\n> ").strip().upper() == 'F':
            usar_linterna(anim_presentes, None)
    else:
        if estado.energia_actual <= 0:
            print(Fore.RED + "\nSin batería. No podés usar cámaras.")
            time.sleep(2)
        else:
            print(Fore.CYAN + "\nPresiona Enter para volver.")
            input()


def usar_linterna(anim_presentes: list, spawn_owner=None):
    """
    Simula el uso de la linterna para retroceder animatrónicos no dueños del spawn.

    Args:
        anim_presentes (list): Animatrónicos presentes.
        spawn_owner (str, optional): Animatrónico dueño del spawn.
    """
    if estado.energia_actual <= 0:
        print(Fore.RED + "¡Sin batería! La linterna no funciona.")
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


# -------------------------- GAME OVER -------------------------- #
def pantalla_game_over(nombre: str):
    """
    Muestra la pantalla de Game Over, reproduciendo sonidos y ASCII art.

    Args:
        nombre (str): Animatrónico responsable del Game Over.
    """
    anim = animatronics[nombre]
    detener_todos_los_canales()

    reproducir_sonido(estado.config["sonido_powerdown"])
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    reproducir_sonido(anim.cancion_muerte)
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    reproducir_sonido(estado.config["sonido_jumpscare"])
    time.sleep(1.5)

    estado.stop_event.set()
    estado.juego_activo = False
    limpiar_pantalla()
    ancho = 80

    mensaje = [
        Fore.RED + Style.BRIGHT + f"¡{nombre.upper()} ENTRÓ A LA OFICINA!".center(ancho),
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
    print(Fore.YELLOW + "Volviendo al menú principal...".center(ancho))
    time.sleep(1)
    from ui.menu import menu_principal
    menu_principal()


# ------------------------------ INTRO ------------------------------ #
def intro():
    """Reproduce la introducción de audio y luego inicia el movimiento de los animatrónicos."""
    reproducir_sonido(estado.config["intro"])
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    for nombre in animatronics:
        Thread(target=mover_animatronico, args=(nombre,), daemon=True).start()


# -------------------------- INSTRUCCIONES -------------------------- #
def mostrar_instrucciones():
    """Muestra las instrucciones del juego en consola."""
    limpiar_pantalla()
    print("\n════════════════════════════════════════")
    print(Style.BRIGHT + Fore.MAGENTA + "📜 INSTRUCCIONES 📜".center(38))
    print("════════════════════════════════════════\n")

    print(Style.BRIGHT + Fore.WHITE + "- Usa las flechas " + Fore.CYAN + "↑ ↓ ← →" + Fore.WHITE + " para moverte por el mapa.\n")
    print(Fore.WHITE + "- Tu objetivo es " + Fore.RED + "sobrevivir la noche" + Fore.WHITE + " vigilando las cámaras.\n")
    print(Fore.WHITE + "- Observa los movimientos de los animatrónicos.\n")
    print(Fore.WHITE + "- Usa la " + Fore.LIGHTYELLOW_EX + "linterna" + Fore.WHITE + " para espantarlos.\n")
    print(Fore.WHITE + "- Si un animatrónico entra en la oficina... " + Fore.RED + Style.BRIGHT + "GAME OVER!\n")
    input(Fore.GREEN + "\nPresiona Enter para volver al menú.")


# -------------------------- DIFICULTAD -------------------------- #
def seleccionar_dificultad():
    """
    Muestra un menú interactivo para seleccionar la dificultad del juego.

    Permite elegir entre NORMAL, DIFÍCIL, PESADILLA o VOLVER al menú principal.
    Cada dificultad modifica:
        - Velocidad de avance de las horas.
        - Consumo de energía por linterna.
        - Consumo de energía por uso de cámara.

    Controles:
        - Flechas arriba/abajo: navegan entre las opciones.
        - Enter: confirma la selección.

    Variables globales:
        estado.config (dict): Diccionario con los parámetros de configuración.
    """
    opciones = ["NORMAL", "DIFÍCIL", "PESADILLA", "VOLVER"]
    colores = [Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.WHITE]
    ancho_pantalla = 60
    seleccion = 0

    while True:
        limpiar_pantalla()

        # Título del menú
        print(Style.BRIGHT + Fore.WHITE + """
                    
        ███╗   ███╗  ██████╗  ██████╗   ██████╗  ███████╗
        ████╗ ████║ ██╔═══██╗ ██╔══██╗ ██╔═══██╗ ██╔════╝
        ██╔████╔██║ ██║   ██║ ██║  ██║ ██║   ██║ ███████╗
        ██║╚██╔╝██║ ██║   ██║ ██║  ██║ ██║   ██║ ╚════██║
        ██║ ╚═╝ ██║ ╚██████╔╝ ██████╔╝ ╚██████╔╝ ███████║
        ╚═╝     ╚═╝  ╚═════╝  ╚═════╝   ╚═════╝  ╚══════╝
        """)

        # Mostrar opciones con la selección actual
        for i, opcion in enumerate(opciones):
            flecha = ">> " if i == seleccion else "   "
            linea = flecha + opcion
            print("\n" + colores[i] + linea.center(ancho_pantalla))

        # Lectura de teclas
        tecla = msvcrt.getch()

        if tecla == b'\xe0':  # Flechas
            flecha = msvcrt.getch()
            if flecha == b'H':  # Arriba
                seleccion = (seleccion - 1) % len(opciones)
            elif flecha == b'P':  # Abajo
                seleccion = (seleccion + 1) % len(opciones)
        elif tecla == b'\r':  # Enter
            if seleccion == 0:  # NORMAL
                estado.config.update({
                    "tiempo_avanzar_hora": 60,
                    "energia_uso_linterna": 5,
                    "energia_uso_camara": 2,
                    "dificultad": "NORMAL"
                })
            elif seleccion == 1:  # DIFÍCIL
                estado.config.update({
                    "tiempo_avanzar_hora": 120,
                    "energia_uso_linterna": 3,
                    "energia_uso_camara": 1.5,
                    "dificultad": "DIFICIL"
                })
            elif seleccion == 2:  # PESADILLA
                estado.config.update({
                    "tiempo_avanzar_hora": 225,
                    "energia_uso_linterna": 2,
                    "energia_uso_camara": 1,
                    "dificultad": "PESADILLA"
                })
            elif seleccion == 3:  # VOLVER
                from ui.menu import menu_principal
                menu_principal()
                return
            time.sleep(1)
            return