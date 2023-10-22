import pygame as pg

from . import ALTO, ANCHO, MAX_NIVELES
from .escenas import Nivel, Portada, Pantalla_records


class TheQuest:
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        # importar las escenas necesarias para jugar: INICIO Y JUEGO (records puede ser llamada tanto desde Inicio como Juego)
        # pasarles como argumento self.pantalla y self.records
        self.nivel = 1
        self.portada = Portada(self.pantalla)
        self.records = Pantalla_records(self.pantalla)

    def jugar(self):

        cerrar_juego = self.records.bucle_principal()
        cerrar_juego = self.portada.bucle_principal()
        if cerrar_juego:
            print("cierro el juego")
            pg.quit()
        else:
            for n in range(0, MAX_NIVELES):
                nivel = Nivel(self.pantalla, n+1)
                cerrar_juego, subir_nivel = nivel.bucle_principal()
                if cerrar_juego:
                    print("cierro el juego desde nivel ", n+1)
                    pg.quit()
                if subir_nivel == False:
                    break

        cerrar_juego = self.records.bucle_principal()
        if cerrar_juego:
            print("saliendo del bucle de thequest.jugar")
            pg.quit()
