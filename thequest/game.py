import pygame as pg

from . import ALTO, ANCHO, MAX_NIVELES
from .escenas import Portada, Pantalla_puntos, Pantalla_records
from .niveles import Nivel


class TheQuest:
    def __init__(self):
        pg.init()
        pg.display.set_caption("THE QUEST")
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.mixer.init()
        self.nivel = 1
        self.portada = Portada(self.pantalla)
        self.pantalla_puntos = Pantalla_puntos(self.pantalla)
        self.pantalla_records = Pantalla_records(self.pantalla)
        # Los niveles se irán instanciando en el método jugar para no instanciar más de los necesarios

    def jugar(self):
        cerrar_juego = False
        while not cerrar_juego:  # QUITAR
            cerrar_juego = self.pantalla_puntos.bucle_principal(
                300000)  # QUITAR
            if not cerrar_juego:  # QUITAR
                cerrar_juego = self.pantalla_records.bucle_principal()  # QUITAR
            cerrar_juego = self.portada.bucle_principal()
            if not cerrar_juego:
                for n in range(0, MAX_NIVELES):
                    nivel = Nivel(self.pantalla, n+1)
                    cerrar_juego, subir_nivel = nivel.bucle_principal()
                    if subir_nivel == False:
                        break
                if not cerrar_juego:
                    cerrar_juego = self.pantalla_puntos.bucle_principal(
                        nivel.puntuacion)
                    if not cerrar_juego:
                        cerrar_juego = self.pantalla_records.bucle_principal()
        pg.quit()
