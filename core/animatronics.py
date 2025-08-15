"""
animatronics.py

Define la clase Animatronico y las instancias de animatrónicos del juego.
Cada animatrónico tiene posición, rutas de movimiento, sonidos y lógica propia.
"""

import random

import core.config as estado
from utils.utils import reproducir_sonido


class Animatronico:
    """
    Representa un animatrónico dentro del juego.

    Atributos:
        nombre (str): Nombre del animatrónico.
        spawn (int): Posición inicial.
        posicion (int): Posición actual.
        ia_level (int): Nivel de IA (1-20).
        intervalo_min (int): Intervalo mínimo de movimiento.
        intervalo_max (int): Intervalo máximo de movimiento.
        rutas (dict): Diccionario de rutas posibles para cada posición.
        pasos_sonido (str): Archivo de sonido de pasos.
        cancion_muerte (str): Archivo de sonido de muerte.
        cara (str): Icono o símbolo que representa al animatrónico.
        canal_pasos (int): Canal de reproducción de pasos.
        acelerado (bool): Indica si el animatrónico está acelerado.
    """

    def __init__(
        self, nombre, spawn, ia_level, intervalo_min, intervalo_max, rutas,
        pasos_sonido, cancion_muerte, cara, canal_pasos
    ):
        """
        Inicializa un animatrónico con sus atributos y configuración.

        Args:
            nombre (str): Nombre del animatrónico.
            spawn (int): Posición inicial.
            ia_level (int): Nivel de IA.
            intervalo_min (int): Intervalo mínimo de movimiento.
            intervalo_max (int): Intervalo máximo de movimiento.
            rutas (dict): Diccionario de rutas de movimiento.
            pasos_sonido (str): Sonido de pasos.
            cancion_muerte (str): Sonido de muerte.
            cara (str): Representación visual del animatrónico.
            canal_pasos (int): Canal de audio para los pasos.
        """
        self.nombre = nombre
        self.spawn = spawn
        self.posicion = spawn
        self.ia_level = ia_level
        self.intervalo_min = intervalo_min
        self.intervalo_max = intervalo_max
        self.rutas = rutas
        self.pasos_sonido = pasos_sonido
        self.cancion_muerte = cancion_muerte
        self.cara = cara
        self.canal_pasos = canal_pasos
        self.acelerado = False

    def mover(self):
        """
        Mueve al animatrónico a una nueva posición posible según su ruta.

        Freddy solo se mueve a partir de las 3 AM. Para otros animatrónicos,
        se puede mantener en la misma posición o moverse a otra de sus rutas.

        Reproduce sonido de pasos si se mueve.
        """
        posibles = self.rutas.get(self.posicion, [])
        if not posibles:
            return

        # Freddy no se mueve antes de las 3AM
        if self.nombre == "Freddy" and estado.hora_actual < 5:
            return

        if self.nombre == "Freddy":
            nueva_posicion = random.choice(posibles)
            reproducir_sonido(self.pasos_sonido, canal=self.canal_pasos)
        else:
            opciones_movimiento = posibles + [self.posicion]
            nueva_posicion = random.choice(opciones_movimiento)
            if nueva_posicion != self.posicion:
                reproducir_sonido(self.pasos_sonido, canal=self.canal_pasos)

        self.posicion = nueva_posicion

    def regresar_spawn(self):
        """
        Devuelve al animatrónico a su posición inicial (spawn).
        """
        self.posicion = self.spawn


# Instancias de animatrónicos del juego
animatronics = {
    "Freddy": Animatronico(
        "Freddy", 2, 8, 4, 7, {
            2: [1],
            1: [3],
            3: [4],
            4: [8]
        },
        "freddy_pasos.mp3", "freddy_song.mp3", "🐻",
        estado.canal_pasos_freddy
    ),
    "Foxy": Animatronico(
        "Foxy", 7, 12, 2, 5, {
            7: [6],
            6: [4, 7],
            4: [8, 6]
        },
        "foxy_pasos.mp3", "foxy_song.mp3", "🦊",
        estado.canal_pasos_foxy
    ),
    "Chica": Animatronico(
        "Chica", 2, 10, 3, 6, {
            2: [1],
            1: [6, 2],
            6: [4, 1],
            4: [8, 6]
        },
        "chica_pasos.mp3", "chica_song.mp3", "🐤",
        estado.canal_pasos_chica
    ),
    "Bonnie": Animatronico(
        "Bonnie", 2, 9, 3, 6, {
            2: [6],
            6: [5, 2],
            5: [7, 6],
            7: [4, 5],
            4: [8, 7]
        },
        "bonnie_pasos.mp3", "bonnie_song.mp3", "🐰",
        estado.canal_pasos_bonnie
    )
}
