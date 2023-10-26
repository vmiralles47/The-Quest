import os
from random import randint, randrange
import pygame as pg

from . import (ANCHO, ALTO, ALTO_MARCADOR, COLOR_OBJETOS,
               DURACION_TURNO, MARGEN_IZQ, NUM_VIDAS, ORIGEN_ASTER,
               VEL_NAVE, VEL_ASTER)


class Nave(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        ruta = os.path.join("resources", "images", "spritesheet_starship.png")
        # surface origen de la que coger los frames
        self.sheet_nave = pg.image.load(ruta)

        # la spritesheet tiene 3 filas de 16 frames cada una, de 100x100 pts.
        ruta_explosion = os.path.join(
            "resources", "images", "explosion_spritesheet_105x105_15fr.png")
        self.sheet_explosion = pg.image.load(ruta_explosion)
        self.surf_explosion = pg.Surface((105, 105))
        self.surf_explosion.set_colorkey((0, 0, 0))
        self.current_frame = 0
        self.frames = 16
        self.frame_width = 100
        self.frame_height = 100
        self.frame_area = (0, 0, self.frame_width, self.frame_height)
        # mi surface a mostrar:
        self.frame_surf = pg.Surface((self.frame_width, self.frame_height))
        alto_inicial = ((ALTO-ALTO_MARCADOR)/2)+(self.frame_height/2)
        self.frame_surf.blit(self.sheet_nave, (0, 0),
                             area=self.frame_area)
        self.rect = self.frame_surf.get_rect(
            midleft=(MARGEN_IZQ, alto_inicial))
        self.frame_surf.set_colorkey((0, 0, 0))
        self.explota = False

    def update(self):
        if self.current_frame > self.frames - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

        frame_area = (self.current_frame*self.frame_width,
                      0, self.frame_width, self.frame_height)
        self.frame_surf.blit(
            self.sheet_nave, (0, 0), area=frame_area)

        pulsadas = pg.key.get_pressed()
        if pulsadas[pg.K_UP]:
            frame_area = (self.current_frame*self.frame_width,
                          200, self.frame_width, self.frame_height)
            self.frame_surf.blit(
                self.sheet_nave, (0, 0), area=frame_area)
            self.rect.y -= VEL_NAVE
            if self.rect.y < ALTO_MARCADOR:
                self.rect.y = ALTO_MARCADOR
        if pulsadas[pg.K_DOWN]:
            frame_area = (self.current_frame*self.frame_width,
                          100, self.frame_width, self.frame_height)
            self.frame_surf.blit(
                self.sheet_nave, (0, 0), area=frame_area)
            self.rect.y += VEL_NAVE
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

    def aterrizar(self):
        # secuencia de movimiento de la nave en el final de nivel
        pass


class Asteroide(pg.sprite.Sprite):

    def __init__(self, tipo, altura):
        # tipo = 1, 2 o 3
        super().__init__()
        self.tipo = tipo
        self.imagenes = []
        for i in range(16):
            if i < 9:
                ruta_img = os.path.join(
                    "resources", "images", f"asteroid{self.tipo}", f"000{i+1}.png")
            else:
                ruta_img = os.path.join(
                    "resources", "images", f"asteroid{self.tipo}", f"00{i+1}.png")
            self.imagenes.append(pg.image.load(ruta_img))
        self.contador = randint(0, len(self.imagenes)-1)
        self.imagen = self.imagenes[self.contador]
        self.rect = self.imagen.get_rect(center=(ORIGEN_ASTER, altura))
        self.velocidad = VEL_ASTER[tipo-1]
        self.turno = randrange(0, DURACION_TURNO)
        # TODO: que los turnos estén mejor espaciados, no pueden coincidir, igual que las alturas

        print("asteroide tipo ", self.tipo,
              "turno = ", self.turno,
              "velocidad ", self.velocidad,
              )

    def update(self, nivel):
        self.contador += 1
        if self.contador > 15:
            self.contador = 0
        self.imagen = self.imagenes[self.contador]

        ha_salido = False
        self.turno = self.turno - 1
        if self.turno < 0:
            self.rect.centerx -= self.velocidad*nivel
        if self.rect.centerx < 0:
            ha_salido = True
        return ha_salido


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


class Fondo():
    # el bucle de fondo infinito lo hago con la misma imagen cargada dos veces
    velocidad_fondo = 10

    def __init__(self):
        ruta = os.path.join("resources", "images",
                            "background", "starmap_2020_4096x720.jpg")
        self.imagen = pg.image.load(ruta)
        self.rect = self.imagen.get_rect(midleft=(0, ALTO/2))

    def update(self):
        # if self.rect.midright == ANCHO+1:

        self.rect.x -= Fondo.velocidad_fondo
