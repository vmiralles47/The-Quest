import pygame as pg

from . import ALTO, ANCHO, MAX_NIVELES
from .escenas import Juego, Portada, Records


class TheQuest:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        # importar las escenas necesarias para jugar: INICIO Y JUEGO (records puede ser llamada tanto desde Inicio como Juego)
        # pasarles como argumento self.pantalla y self.records
        self.nivel = 1
        self.portada = Portada(self.pantalla)
        self.juego = Juego(self.pantalla)
        self.records = Records(self.pantalla)

    def jugar(self):
        cerrar_juego = self.portada.bucle_principal()
        if cerrar_juego:
            print("saliendo del bucle de thequest.jugar")
            pg.quit()
        else:
            cerrar_juego = self.juego.bucle_principal()
            if cerrar_juego:
                print("saliendo del bucle de thequest.jugar")
                pg.quit()
            else:
                cerrar_juego = self.records.bucle_principal()
                if cerrar_juego:
                    print("saliendo del bucle de thequest.jugar")
                    pg.quit()
