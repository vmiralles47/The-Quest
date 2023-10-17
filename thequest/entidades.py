import os
from random import randint, randrange

import pygame as pg


from . import ANCHO, ALTO, COLOR_OBJETOS, MARGEN_IZQ, VEL_NAVE


class Nave():

    def __init__(self):
        ruta = os.path.join("resources", "rocket_100_largo.png")
        # self.imagen_nave es de tipo surface
        self.imagen_nave = pg.image.load(ruta)
        self.rect = self.imagen_nave.get_rect(midleft=(MARGEN_IZQ, ALTO/2))

    def update(self):
        pulsadas = pg.key.get_pressed()
        if pulsadas[pg.K_UP]:
            self.rect.y -= VEL_NAVE
            if self.rect.y < 0:
                self.rect.y = 0
        if pulsadas[pg.K_DOWN]:
            self.rect.y += VEL_NAVE
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

    def explotar(self):
        # carga la sec de imagenes de la explosión
        pass

    def aterrizar(self):
        # secuencia de movimiento de la nave en el final de nivel
        pass


class Asteroide():

    def __init__(self, pos_x, pos_y, radio, velocidad):
        self.radio = radio
        self.color = COLOR_OBJETOS
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocidad = velocidad
        self.turno = randrange(0, 2000, 50)

    def update(self):
        self.turno = self.turno - 1
        if self.turno < 0:
            self.pos_x -= self.velocidad

    def pintar(self, pantalla):
        pg.draw.circle(pantalla, self.color,
                       (self.pos_x, self.pos_y), self.radio, width=2)
