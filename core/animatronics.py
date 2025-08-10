from utils.utils import reproducir_sonido
import core.config as estado
import random

class Animatronico:
    
    """
        Representa un animatrónico dentro del juego, con su posición, rutas de movimiento,
        sonido asociado y lógica propia de movimiento.
    """

    def __init__(self, nombre, spawn, ia_level, intervalo_min, intervalo_max, rutas, pasos_sonido, cancion_muerte, cara, canal_pasos):
        self.nombre = nombre
        self.spawn = spawn
        self.posicion = spawn
        self.ia_level = ia_level # Nivel de IA (1-20)
        self.intervalo_min = intervalo_min
        self.intervalo_max = intervalo_max
        self.rutas = rutas
        self.pasos_sonido = pasos_sonido
        self.cancion_muerte = cancion_muerte
        self.cara = cara,
        self.canal_pasos = canal_pasos  
        self.acelerado = False

    def mover(self):
        
        """
            Mueve al animatrónico a una nueva posición posible según su ruta.
            Freddy solo se mueve a partir de las 3 AM.
        """
        
        posibles = self.rutas.get(self.posicion, [])
        if not posibles:
            return

        # Freddy no se mueve antes de las 3AM
        if self.nombre == "Freddy" and estado.hora_actual < 3:
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


animatronics = {
    "Freddy": Animatronico("Freddy", 2, 8, 4, 7,{
        2: [1],
        1: [3],
        3: [4],
        4: [8]
    }, "freddy_pasos.mp3", "freddy_song.mp3", "🐻", estado.canal_pasos_freddy),

    "Foxy": Animatronico("Foxy", 7, 12, 2, 5, {
        7: [6],
        6: [4, 7],
        4: [8, 6]
    }, "foxy_pasos.mp3", "foxy_song.mp3", "🦊", estado.canal_pasos_foxy),

    "Chica": Animatronico("Chica", 2, 10, 3, 6, {
        2: [1],
        1: [6, 2],
        6: [4, 1],
        4: [8, 6]
    }, "chica_pasos.mp3", "chica_song.mp3", "🐤", estado.canal_pasos_chica),

    "Bonnie": Animatronico("Bonnie", 2, 9, 3, 6, {
        2: [6],
        6: [5, 2],
        5: [7, 6],
        7: [4, 5],
        4: [8, 7]
    }, "bonnie_pasos.mp3", "bonnie_song.mp3", "🐰", estado.canal_pasos_bonnie)
}
