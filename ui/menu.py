from utils.utils import limpiar_pantalla
import core.config as estado
from core.game_engine import iniciar_juego
from ui.screens import mostrar_instrucciones

import sys
import time
import msvcrt

from colorama import init, Fore, Style
init(autoreset=True)


def menu_principal():

    """
        Muestra el menú principal interactivo del juego y gestiona la navegación del usuario.

        La función despliega un menú con tres opciones: "INICIAR NOCHE", "INSTRUCCIONES" y "SALIR", 
        permitiendo al usuario navegar entre ellas con las teclas de flecha arriba y abajo. 
        La opción seleccionada se resalta con colores diferentes.

        Al presionar Enter:
            - "INICIAR NOCHE" llama a la función `iniciar_juego()` y sale del menú.
            - "INSTRUCCIONES" llama a la función `mostrar_instrucciones()`.
            - "SALIR" muestra un mensaje de despedida, limpia la pantalla y termina la ejecución.

        Notas:
            - Usa `msvcrt.getch()` para capturar la entrada del teclado en Windows.
            - El menú se ejecuta en un bucle infinito hasta que el usuario selecciona salir o inicia el juego.
            - Limpia la pantalla antes de mostrar el menú cada vez.
            - Usa colores y estilos para mejorar la visualización en consola.

        Args:
            Ninguno.

        Variables locales:
            ancho_pantalla (int): Ancho para centrar el texto del menú.
            opciones (list): Lista de opciones disponibles en el menú.
            seleccion (int): Índice de la opción actualmente seleccionada.
    """

    estado.motivo_game_over = None

    ancho_pantalla = 60
    opciones = ["INICIAR NOCHE", "INSTRUCCIONES", "SALIR"]
    seleccion = 0
    while True:
        limpiar_pantalla()
        
        
        print(Style.BRIGHT + Fore.WHITE + """
                    
              ███████╗ ███╗   ██╗  █████╗  ███████╗
              ██╔════╝ ████╗  ██║ ██╔══██╗ ██╔════╝
              █████╗   ██╔██╗ ██║ ███████║ █████╗  
              ██╔══╝   ██║╚██╗██║ ██╔══██║ ██╔══╝  
              ██║      ██║ ╚████║ ██║  ██║ ██║     
              ╚═╝      ╚═╝  ╚═══╝ ╚═╝  ╚═╝ ╚═╝                               
                         CMD NIGHT GAME      
        """)
         # Opciones
        for i, opcion in enumerate(opciones):
            if i == seleccion:
                flecha = ">> "
            else:
                flecha = "   "

            if i == 0:
                color = Fore.GREEN
            elif i == 1:
                color = Fore.YELLOW
            else:
                color = Fore.RED
            
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
                print(Fore.GREEN + Style.BRIGHT + "\n¡Hasta la próxima, vigilante nocturno!")
                time.sleep(1.5)
                limpiar_pantalla()
                sys.exit()
