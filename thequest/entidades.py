import os
from random import randint

import pygame as pg


from . import ANCHO, ALTO, COLOR_OBJETOS, MARGEN_IZQ


class Nave():

    velocidad = 15

    def __init__(self):
        ruta = os.path.join("resources", "rocket_100_largo.png")
        # self.imagen_nave es de tipo surface
        self.imagen_nave = pg.image.load(ruta)
        self.rect = self.imagen_nave.get_rect(midleft=(MARGEN_IZQ, ALTO/2))

    def update(self):
        pulsadas = pg.key.get_pressed()
        if pulsadas[pg.K_UP]:
            self.rect.y -= self.velocidad
            if self.rect.y < 0:
                self.rect.y = 0
        if pulsadas[pg.K_DOWN]:
            self.rect.y += self.velocidad
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

    def explotar(self):
        # carga la sec de imagenes de la explosión
        pass

    def aterrizar(self):
        # secuencia de movimiento de la nave en el final de nivel
        pass
