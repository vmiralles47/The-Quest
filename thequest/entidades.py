import os
from random import randint, randrange
import pygame as pg

from . import (ANCHO, ALTO, ALTO_MARCADOR, COLOR_OBJETOS,
               DURACION_TURNO, MARGEN_IZQ, MAX_NIVELES, NUM_VIDAS, ORIGEN_ASTER,
               VEL_FACTOR_INERCIA, VEL_NAVE, VEL_ASTER, VEL_PLANETA)


class Nave(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        ruta = os.path.join("resources", "images", "spritesheet_starship.png")
        # surface origen de la que coger los frames
        self.sheet_nave = pg.image.load(ruta)
        # la spritesheet tiene 3 filas de 16 frames cada una, de 100x100 pts.
        self.current_frame = 0
        self.frames = 16
        self.frame_width = 100
        self.frame_height = 100
        self.frame_area = (0, 0, self.frame_width, self.frame_height)
        # mi surface a mostrar:
        self.imagen = pg.Surface((self.frame_width, self.frame_height))
        self.imagen_aux = pg.Surface((self.frame_width, self.frame_height))
        self.imagen_aux2 = pg.Surface((self.frame_width, self.frame_height))
        alto_inicial = ((ALTO-ALTO_MARCADOR)/2)+(self.frame_height/2)
        self.imagen.blit(self.sheet_nave, (0, 0),
                         area=self.frame_area)
        self.rect = self.imagen.get_rect(
            midleft=(MARGEN_IZQ, alto_inicial))
        self.rect_aux = self.imagen.get_rect(
            midleft=(MARGEN_IZQ, alto_inicial))
        self.imagen.set_colorkey((0, 0, 0))
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
                      0, self.frame_width, self.frame_height)
        self.imagen.blit(
            self.sheet_nave, (0, 0), area=frame_area)

        self.se_mueve = False
        pulsadas = pg.key.get_pressed()

        if pulsadas[pg.K_UP]:
            frame_area = (self.current_frame*self.frame_width,
                          200, self.frame_width, self.frame_height)
            self.imagen.blit(
                self.sheet_nave, (0, 0), area=frame_area)
            print("subiendo A velocidad", self.velocidad)
            self.rect.y -= self.velocidad
            self.velocidad += VEL_FACTOR_INERCIA
            self.se_mueve = True

        if self.rect.y < ALTO_MARCADOR:
            self.rect.y = ALTO_MARCADOR

        if pulsadas[pg.K_DOWN]:
            frame_area = (self.current_frame*self.frame_width,
                          100, self.frame_width, self.frame_height)
            self.imagen.blit(
                self.sheet_nave, (0, 0), area=frame_area)
            print("bajando velocidad:  ", self.velocidad)
            self.rect.y += self.velocidad
            self.velocidad += VEL_FACTOR_INERCIA
            self.se_mueve = True
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO
        return self.se_mueve

    def update_explosion(self):
        if self.contador_explosion == 30:
            self.contador_explosion = 0
            return False
        else:
            self.contador_explosion += 1
            frame_area = (self.contador_explosion*105, 0, 105, 105)
            self.imagen.blit(self.sheet_explosion, (0, 0), frame_area)
            return True

    def update_rotacion(self, lugar_aterrizaje):
        angulo_rotacion = 9

        if self.angulo_rotado < 180:

            self.imagen_aux = pg.transform.rotate(
                self.imagen, angulo_rotacion*self.contador_angulo
            )
            self.rect_aux = self.imagen_aux.get_rect(center=(self.rect.center))
            self.angulo_rotado += angulo_rotacion
            self.contador_angulo += 1

            print("centro rect nvae", self.rect.center)
            print("cenrto rect aux", self.rect_aux.center)
            print("ROTACION:", self.angulo_rotado)
            return False
        elif self.rect_aux.centerx < ANCHO - ((ANCHO - lugar_aterrizaje)/2):
            self.rect_aux.centerx += VEL_NAVE
        else:
            return True

    def update_va_al_centro(self):
        # secuencia de movimiento de la nave en el final de nivel.va hasta el centro desde donde esté
        if self.current_frame > self.frames - 1:
            self.current_frame = 0
        else:
            self.current_frame += 1

        frame_area = (self.current_frame*self.frame_width,
                      0, self.frame_width, self.frame_height)
        self.imagen.blit(
            self.sheet_nave, (0, 0), area=frame_area)

        distancia_centro_y = (ALTO/2 - self.rect.centery)
        distancia_centro_x = (ANCHO/2 - self.rect.centerx)
        vel_y = int(distancia_centro_y / 10)
        vel_x = int(distancia_centro_x / 10)
        self.rect.x += vel_x
        self.rect.y += vel_y

        if int(self.rect.y+50) in range(int((ALTO/2)-10), int((ALTO/2)+10)):
            vel_y = 0
            vel_x = 0
            print("estoy en el centro")
            return True  # ya está en el centro. Lisyo esté listo para rotar
        else:
            return False


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
    velocidad_fondo = 8

    def __init__(self):
        ruta = os.path.join("resources", "images",
                            "background", "starmap_2020_4096x720.jpg")
        self.imagen = pg.image.load(ruta)
        self.rect = self.imagen.get_rect(midleft=(0, ALTO/2))

    def update(self):
        # if self.rect.midright == ANCHO+1:

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
