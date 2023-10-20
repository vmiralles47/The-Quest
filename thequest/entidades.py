import os
from random import randint, randrange

import pygame as pg


from . import ANCHO, ALTO, ALTO_MARCADOR, COLOR_OBJETOS, DURACION_TURNO, MARGEN_IZQ, NUM_VIDAS, ORIGEN_ASTER, RAD_ASTER, VEL_NAVE, VEL_ASTER


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
            if self.rect.y < ALTO_MARCADOR:
                self.rect.y = ALTO_MARCADOR
        if pulsadas[pg.K_DOWN]:
            self.rect.y += VEL_NAVE
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

    def explotar(self):
        # carga la sec de imagenes de la explosión
        self.rect.y = (ALTO-ALTO_MARCADOR)/2

    def aterrizar(self):
        # secuencia de movimiento de la nave en el final de nivel
        pass


class Asteroide():

    def __init__(self, tipo, altura):
        self.tipo = tipo
        self.radio = RAD_ASTER[tipo-1]
        self.color = COLOR_OBJETOS
        self.pos_x = ORIGEN_ASTER
        self.pos_y = altura
        self.velocidad = VEL_ASTER[tipo-1]
        self.turno = randrange(0, DURACION_TURNO)
        # TODO: que los turnos estén mejor espaciados, no pueden coincidir, igual que las alturas
        self.rect = pg.rect.Rect(0, 0, 0, 0)
        print("asteroide tipo ", self.tipo,
              "turno = ", self.turno,
              "radio ", self.radio,
              "velocidad ", self.velocidad,
              "altura ", self.pos_y)

    def update(self, nivel):
        ha_salido = False
        self.turno = self.turno - 1
        if self.turno < 0:
            self.pos_x -= self.velocidad*nivel
        if self.pos_x < 0:
            ha_salido = True
        return ha_salido

    def pintar(self, pantalla):
        self.rect = pg.draw.circle(pantalla, self.color,
                                   (self.pos_x, self.pos_y), self.radio, width=2)


class Marcador():
    def __init__(self, puntos_de_inicio):
        self.total = puntos_de_inicio
        fuente = "Square.ttf"
        ruta = os.path.join("resources", "fonts", fuente)
        self.tipo = pg.font.Font(ruta, 40)

    def incrementar(self, incremento):
        self.total += incremento

    def pintar(self, pantalla):
        r = pg.rect.Rect(0, 0, ANCHO/2, ALTO_MARCADOR)
        pg.draw.rect(pantalla, (0, 0, 0), r)
        puntuacion = str(self.total)
        texto = self.tipo.render(puntuacion, True, COLOR_OBJETOS)
        pos_x = MARGEN_IZQ
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        pantalla.blit(texto, (pos_x, pos_y))


class Contador_Vidas():
    def __init__(self, vidas_iniciales):
        self.total_vidas = vidas_iniciales
        fuente = "Square.ttf"
        ruta = os.path.join("resources", "fonts", fuente)
        self.tipo = pg.font.Font(ruta, 40)

    def restar_vida(self):
        self.total_vidas -= 1

    def pintar(self, pantalla):
        r = pg.rect.Rect(ANCHO/2, 0, ANCHO, ALTO_MARCADOR)
        pg.draw.rect(pantalla, (0, 0, 0), r)
        vidas = str(self.total_vidas)
        texto = self.tipo.render(vidas, True, COLOR_OBJETOS)
        pos_x = ANCHO - 100
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        pantalla.blit(texto, (pos_x, pos_y))

    def consultar(self):
        return self.total_vidas

    def resetear(self):
        self.total_vidas = NUM_VIDAS
