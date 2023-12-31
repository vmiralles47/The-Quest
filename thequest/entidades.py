import os
from random import randint
import pygame as pg

from . import (ANCHO, ALTO, ALTO_MARCADOR, MARGEN_IZQ, MAX_NIVELES,
               NUM_VIDAS, ORIGEN_ASTER, RUTA_TIPOGRAFIA, VEL_ASTER, VEL_FACTOR_INERCIA,
               VEL_MAX_NAVE, VEL_NAVE, VEL_PLANETA)


class Nave(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        ruta = os.path.join("resources", "images", "spritesheet_starship.png")
        # surface origen de la que coger los frames
        self.sheet_nave = pg.image.load(ruta)
        # la spritesheet tiene 3 filas de 16 frames cada una, de 100x100 pts.imagen válida 70 pts de alto
        self.current_frame = 0
        self.frames = 16
        self.frame_width = 100
        self.nave_frame_height = 70
        # mi surface a mostrar:
        self.imagen_nave = pg.Surface(
            (self.frame_width, self.nave_frame_height))
        self.nave_frame_area = (0, 15, self.frame_width,
                                self.nave_frame_height)
        self.imagen_nave.blit(self.sheet_nave, (0, 0),
                              area=self.nave_frame_area)
        self.imagen_nave.set_colorkey((0, 0, 0))
        alto_inicial = ((ALTO-ALTO_MARCADOR)/2)+(self.nave_frame_height/2)
        self.rect = self.imagen_nave.get_rect(
            midleft=(MARGEN_IZQ, alto_inicial))

        # surface auxiliar 100 x 100 para la explosion y la rotacion:
        self.aux_frame_height = 100
        self.imagen_aux = pg.Surface((self.frame_width, self.aux_frame_height))
        self.aux_frame_area = (0, 15, self.frame_width, self.aux_frame_height)
        self.rect_aux = self.imagen_aux.get_rect(
            midleft=(MARGEN_IZQ, alto_inicial))
        self.imagen_aux.set_colorkey((0, 0, 0))
        # spritesheet de la explosion, una fila de 21 elementos de 105x105 cada uno
        ruta_explosion = os.path.join(
            "resources", "images", "explosion_spritesheet_105x105_15fr.png")
        self.sheet_explosion = pg.image.load(ruta_explosion)
        self.contador_explosion = 0
        self.explota = False
        self.contador_angulo = 1
        self.angulo_rotado = 0
        self.velocidad = VEL_NAVE
        self.se_mueve = False  # testigo booleano apra la velocidad inercial
        ruta_sound = os.path.join("resources", "sounds", "fireball.mp3")
        self.sonido_explosion = pg.mixer.Sound(ruta_sound)
        ruta_sonidoreactor = os.path.join(
            "resources", "sounds", "motor_nave.mp3")
        self.sonido_reactor = pg.mixer.Sound(ruta_sonidoreactor)
        self.sonido_reactor_on = False

    def update(self):
        if self.current_frame > self.frames - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

        frame_area = (self.current_frame*self.frame_width,
                      15, self.frame_width, self.nave_frame_height)
        self.imagen_nave.blit(
            self.sheet_nave, (0, 0), area=frame_area)

        self.se_mueve = False
        pulsadas = pg.key.get_pressed()

        if pulsadas[pg.K_UP]:
            frame_area = (self.current_frame*self.frame_width,
                          215, self.frame_width, self.nave_frame_height)
            self.imagen_nave.blit(
                self.sheet_nave, (0, 0), area=frame_area)

            self.rect.y -= self.velocidad
            if self.velocidad <= VEL_MAX_NAVE:
                self.velocidad += VEL_FACTOR_INERCIA
            self.se_mueve = True

        if self.rect.y < ALTO_MARCADOR:
            self.rect.y = ALTO_MARCADOR

        if pulsadas[pg.K_DOWN]:
            frame_area = (self.current_frame*self.frame_width,
                          115, self.frame_width, self.nave_frame_height)
            self.imagen_nave.blit(
                self.sheet_nave, (0, 0), area=frame_area)
            self.rect.y += self.velocidad
            if self.velocidad <= VEL_MAX_NAVE:
                self.velocidad += VEL_FACTOR_INERCIA
            self.se_mueve = True
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO
        return self.se_mueve

    def update_explosion(self):
        NUM_IMAGENES = 21
        ANCHO_FRAME_EXPL = 105
        if self.contador_explosion == NUM_IMAGENES:
            self.contador_explosion = 0
            return False
        else:
            self.contador_explosion += 1
            frame_area = (self.contador_explosion*ANCHO_FRAME_EXPL,
                          15, ANCHO_FRAME_EXPL, ANCHO_FRAME_EXPL)
            self.imagen_aux.blit(self.sheet_explosion, (0, 0), frame_area)
            return True

    def update_rotacion(self, lugar_aterrizaje):
        angulo_rotacion = 9
        if self.angulo_rotado < 180:
            self.imagen_aux = pg.transform.rotate(
                self.imagen_nave, angulo_rotacion*self.contador_angulo
            )
            self.rect_aux = self.imagen_aux.get_rect(
                center=(self.rect.center))
            self.angulo_rotado += angulo_rotacion
            self.contador_angulo += 1
            return False
        elif self.rect_aux.centerx < ANCHO - ((ANCHO - lugar_aterrizaje)/2):
            self.rect_aux.centerx += VEL_NAVE
            return False
        else:
            return True

    def update_va_al_centro(self):
        # secuencia de movimiento de la nave en el final de nivel.va hasta el centro desde donde esté
        if self.current_frame > self.frames - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

        frame_area = (self.current_frame*self.frame_width,
                      15, self.frame_width, self.nave_frame_height)
        self.imagen_nave.blit(
            self.sheet_nave, (0, 0), area=frame_area)

        distancia_centro_y = (ALTO/2 - self.rect.centery)
        distancia_centro_x = (ANCHO/2 - self.rect.centerx)
        vel_y = int(distancia_centro_y / 10)
        vel_x = int(distancia_centro_x / 10)
        self.rect.x += vel_x
        self.rect.y += vel_y
        if int(self.rect.centery) in range(int((ALTO/2)-10), int((ALTO/2)+10)):
            vel_y = 0
            vel_x = 0
            return True  # ya está en el centro, lista para rotar
        else:
            return False


class Asteroide(pg.sprite.Sprite):

    def __init__(self, altura, tipo, turno):
        # tipo = 1, 2 o 3
        super().__init__()
        self.tipo = tipo
        self.imagenes = []
        for i in range(15):
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
        self.turno = turno

    def update(self, nivel):
        self.contador += 1
        if self.contador > 14:
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
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, 40)

    def incrementar(self, incremento):
        self.total += incremento

    def consultar(self):
        return self.total


class Contador_Niveles():
    def __init__(self, niveles_iniciales):
        self.total_niveles = niveles_iniciales

    def restar_nivel(self):
        self.total_niveles -= 1

    def consultar(self):
        return self.total_niveles

    def resetear(self):
        self.total_niveles = MAX_NIVELES


class Contador_Vidas():
    def __init__(self, vidas_iniciales):
        self.total_vidas = vidas_iniciales

    def restar_vida(self):
        self.total_vidas -= 1

    def consultar(self):
        return self.total_vidas

    def resetear(self):
        self.total_vidas = NUM_VIDAS


class Fondo():
    # el bucle de fondo infinito lo hago con la misma imagen cargada dos veces
    velocidad_fondo = 6

    def __init__(self):
        ruta = os.path.join("resources", "images",
                            "background", "starmap_2020_4096x720.jpg")
        self.imagen = pg.image.load(ruta)
        self.rect = self.imagen.get_rect(midleft=(0, ALTO/2))

    def update(self):

        self.rect.x -= Fondo.velocidad_fondo


class Planeta():
    def __init__(self, nivel):
        ruta = os.path.join("resources", "images",
                            "planets", f"planet{nivel}.png")
        self.imagen = pg.image.load(ruta)
        self.rect = self.imagen.get_rect()
        ancho_imagen = self.imagen.get_width()
        self.rect.centerx = ANCHO + ancho_imagen/2
        self.rect.centery = ALTO/2
        self.nivel = nivel
        if nivel == 4:
            ruta_musica = os.path.join("resources", "sounds",
                                       "musica_nivel4.mp3")
            self.musica_nivel4 = pg.mixer.Sound(ruta_musica)
        self.play_music = False

    def update(self):
        if self.rect.centerx > ANCHO:
            self.rect.centerx -= VEL_PLANETA
        return self.rect.left

    def play_music_nivel4(self):
        if self.play_music == False:
            self.musica_nivel4.play()
            self.play_music = True
