"""
menu_principal.py

Muestra el menú principal interactivo del juego y gestiona la navegación del usuario.
"""

import sys
import time
import msvcrt

from colorama import init, Fore, Style
init(autoreset=True)

import core.config as estado
from core.game_engine import iniciar_juego
from ui.screens import mostrar_instrucciones
from utils.utils import limpiar_pantalla


def menu_principal():
    """
    Muestra el menú principal interactivo y gestiona la navegación del usuario.

    Despliega un menú con tres opciones: "INICIAR NOCHE", "INSTRUCCIONES" y "SALIR".
    Permite navegar entre ellas con las flechas arriba/abajo y seleccionar con Enter.

    Comportamiento al seleccionar una opción:
        - "INICIAR NOCHE": Llama a `iniciar_juego()` y sale del menú.
        - "INSTRUCCIONES": Llama a `mostrar_instrucciones()`.
        - "SALIR": Muestra mensaje de despedida, limpia la pantalla y termina la ejecución.

    Notas:
        - Usa `msvcrt.getch()` para capturar la entrada del teclado en Windows.
        - Limpia la pantalla antes de mostrar el menú cada vez.
        - Resalta la opción seleccionada con colores y estilos.
        - Se ejecuta en un bucle hasta que el usuario inicia el juego o sale.

    Variables locales:
        ancho_pantalla (int): Ancho para centrar el texto del menú.
        opciones (list): Lista de opciones del menú.
        seleccion (int): Índice de la opción actualmente seleccionada.
    """
    estado.motivo_game_over = None

    ancho_pantalla = 60
    opciones = ["INICIAR NOCHE", "INSTRUCCIONES", "SALIR"]
    seleccion = 0

    while True:
        limpiar_pantalla()

        # Título
        print(Style.BRIGHT + Fore.WHITE + """
                    
              ███████╗ ███╗   ██╗  █████╗  ███████╗
              ██╔════╝ ████╗  ██║ ██╔══██╗ ██╔════╝
              █████╗   ██╔██╗ ██║ ███████║ █████╗  
              ██╔══╝   ██║╚██╗██║ ██╔══██║ ██╔══╝  
              ██║      ██║ ╚████║ ██║  ██║ ██║     
              ╚═╝      ╚═╝  ╚═══╝ ╚═╝  ╚═╝ ╚═╝                               
                           SIGNAL LOST      
        """)

        # Opciones
        for i, opcion in enumerate(opciones):
            flecha = ">> " if i == seleccion else "   "
            color = Fore.GREEN if i == 0 else Fore.YELLOW if i == 1 else Fore.RED
            linea = flecha + opcion
            print("\n" + color + Style.BRIGHT + linea.center(ancho_pantalla))

        # Leer tecla
        tecla = msvcrt.getch()

        if tecla == b'\xe0':  # Tecla especial (flechas)
            flecha = msvcrt.getch()
            if flecha == b'H':  # Flecha arriba
                seleccion = (seleccion - 1) % len(opciones)
            elif flecha == b'P':  # Flecha abajo
                seleccion = (seleccion + 1) % len(opciones)

        elif tecla == b'\r':  # Enter
            if seleccion == 0:
                iniciar_juego()
                break
            elif seleccion == 1:
                mostrar_instrucciones()
            elif seleccion == 2:
                print(Fore.GREEN + Style.BRIGHT +
                      "\n¡Hasta la próxima, vigilante nocturno!")
                time.sleep(1.5)
                limpiar_pantalla()
                sys.exit()
