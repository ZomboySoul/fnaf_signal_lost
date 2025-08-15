"""
utils.py

Módulo de utilidades para el juego Freddy's Family Diner.

Funciones incluidas:
- resource_path(): Resuelve rutas absolutas para recursos.
- limpiar_pantalla(): Limpia la consola.
- reproducir_sonido(): Reproduce sonidos con Pygame.
- cargar_plantilla_archivo(): Carga plantillas de las cámaras.
"""

import os
import sys
import warnings
import core.config as estado

# ---------------------- CONFIGURACIÓN INICIAL ---------------------- #
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
warnings.filterwarnings("ignore", category=UserWarning)
import pygame
pygame.init()


def resource_path(relative_path):
    """
    Resuelve la ruta absoluta a un recurso, compatible con PyInstaller.

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
    Limpia la pantalla de la consola, compatible con Windows y Unix.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def reproducir_sonido(archivo, canal=None):
    """
    Reproduce un sonido desde el archivo especificado.

    Args:
        archivo (str): Nombre del archivo de sonido.
        canal (pygame.mixer.Channel, opcional): Canal específico para reproducir el sonido.
    """
    try:
        ruta = resource_path(
            os.path.join(estado.config.get("carpeta_sonidos", ""), archivo)
        )
        if not os.path.isfile(ruta):
            print(f"[WARNING] Archivo de sonido no encontrado: {ruta}")
            return

        sonido = pygame.mixer.Sound(ruta)
        if canal:
            canal.play(sonido)
        else:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play()
    except Exception as e:
        print(f"[ERROR] No se pudo reproducir {archivo}: {e}")


def cargar_plantilla_archivo(camara_num, anim_presentes):
    """
    Carga la plantilla de texto de una cámara según los animatrónicos presentes.

    Args:
        camara_num (int): Número de la cámara a cargar.
        anim_presentes (list of str): Lista de nombres de animatrónicos presentes.

    Returns:
        list of str: Líneas leídas del archivo de plantilla.
    """
    carpeta_base = estado.config.get("carpeta_rooms", "")
    carpeta = os.path.join(carpeta_base, f"CAM_{str(camara_num).zfill(2)}")

    if not anim_presentes:
        combinacion = "EMPTY"
    else:
        combinacion = "_".join(sorted(anim_presentes))

    ruta = os.path.join(carpeta, f"{combinacion}.txt")
    if not os.path.isfile(ruta):
        ruta = os.path.join(carpeta, "EMPTY.txt")
        if not os.path.isfile(ruta):
            print(f"[WARNING] No se encontró plantilla para CAM_{camara_num}")
            return []

    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    return lineas
