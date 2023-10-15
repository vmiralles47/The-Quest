import pygame as pg

from . import ALTO, ANCHO
from .escenas import Juego, Portada, Records


class TheQuest:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        # importar las escenas necesarias para jugar: INICIO Y JUEGO (records puede ser llamada tanto desde Inicio como Juego)
        # pasarles como argumento self.pantalla y self.records
        portada = Portada(self.pantalla)
        juego = Juego(self.pantalla)
        records = Records(self.pantalla)
        self.escenas = [portada, juego, records]

    def jugar(self):
        for escena in self.escenas:
            he_acabado = escena.bucle_principal()
            if he_acabado:
                break
        print("saliendo del bucle de thequest.jugar")
        pg.quit()
