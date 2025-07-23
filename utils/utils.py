import core.config  as estado

import sys, os
import pygame
pygame.init()

def resource_path(relative_path):
    
    """
        Resuelve la ruta absoluta a un recurso, compatible con entornos empaquetados (PyInstaller).

        Args:
            relative_path (str): Ruta relativa al archivo.

        Returns:
            str: Ruta absoluta al recurso.
    """

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def limpiar_pantalla():

    """
        Limpia la pantalla de la consola.
    """
        
    os.system('cls' if os.name == 'nt' else 'clear')


def reproducir_sonido(archivo, canal=None):

    """
        Reproduce un sonido desde el archivo especificado.

        Args:
            archivo (str): Nombre del archivo de sonido.
            canal (Channel, opcional): Canal específico de Pygame para reproducir el sonido.
    """

    try:
        ruta = resource_path(os.path.join(estado.config["carpeta_sonidos"], archivo))
        sonido = pygame.mixer.Sound(ruta)

        if canal:
            canal.play(sonido)
        else:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play()

    except Exception as e:
        print(f"No se pudo reproducir {archivo}: {e}")


def cargar_plantilla_archivo(camara_num, anim_presentes):
   
    """
        Carga la plantilla de texto correspondiente a una cámara y los animatrónicos presentes.

        Busca un archivo de plantilla en la carpeta específica de la cámara `camara_num`. 
        El nombre del archivo se determina según los animatrónicos presentes (`anim_presentes`), 
        concatenados en orden alfabético separados por guiones bajos. 

        Si no hay animatrónicos presentes, se usa la plantilla "EMPTY.txt". 
        Si el archivo esperado no existe, se carga la plantilla "EMPTY.txt" por seguridad.

        Args:
            camara_num (int): Número de la cámara a cargar.
            anim_presentes (list of str): Lista de nombres de animatrónicos presentes en la cámara.

        Returns:
            list of str: Líneas leídas del archivo de plantilla correspondiente.

        Notas:
            - Se asume que la configuración `config["carpeta_rooms"]` define la ruta base de las cámaras.
            - Los archivos se leen con codificación UTF-8.
    """

    carpeta = os.path.join(estado.config["carpeta_rooms"], f"CAM_{str(camara_num).zfill(2)}")
    if not anim_presentes:
        combinacion = "EMPTY"
    else:
        combinacion = "_".join(sorted(anim_presentes))
    ruta = os.path.join(carpeta, f"{combinacion}.txt")
    if not os.path.isfile(ruta):
        # si no existe el archivo, cargar EMPTY por seguridad
        ruta = os.path.join(carpeta, "EMPTY.txt")
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    return lineas
