import os

import pygame as pg

from . import (ANCHO, ALTO, COLOR_OBJETOS, MENSAJE_PORTADA, RUTA_TIPOGRAFIA)
from .records import Records


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()
        pg.init()

    def bucle_principal(self):
        """
        método para ser implementado por cada escena, 
        en función de lo que estén esperando hastala condición de salida
        """

    def barra_pulsada(self, evento):
        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
            return True

    def pintar_mensaje(self, cadena, tamanio, altura_opc=0):
        tipo = pg.font.Font(RUTA_TIPOGRAFIA, tamanio)
        mensaje = cadena
        lineas = mensaje.splitlines()
        altura_tipo = tipo.get_height()
        contador = 0
        if altura_opc != 0:
            factor_altura = altura_opc
        else:
            factor_altura = ALTO/2
        for linea in lineas:
            texto_imagen = tipo.render(linea, True, COLOR_OBJETOS)
            x = (ANCHO-texto_imagen.get_width())/2
            y = factor_altura + contador*altura_tipo
            contador += 1
            self.pantalla.blit(texto_imagen, (x, y))

    def pintar_mensaje_barra(self):
        tipo = pg.font.Font(RUTA_TIPOGRAFIA, 15)
        mensaje = "Pulsa ESPACIO para continuar"
        texto_imagen = tipo.render(mensaje, True, COLOR_OBJETOS, (0, 0, 0))
        x = (ANCHO-texto_imagen.get_width())/2
        y = 5*(ALTO/6)
        self.pantalla.blit(texto_imagen, (x, y))

    def pintar_logo(self):
        tipo = pg.font.Font(RUTA_TIPOGRAFIA, 100)
        mensaje = "THE QUEST"
        texto_imagen = tipo.render(mensaje, True, COLOR_OBJETOS)
        x = (ANCHO - texto_imagen.get_width())/2
        y = (ALTO - texto_imagen.get_height())/4
        self.pantalla.blit(texto_imagen, (x, y))


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta = os.path.join("resources", "images",
                            "background", "fondo_portada.jpg")
        self.imagen = pg.image.load(ruta)
        ruta_musica = os.path.join("resources", "sounds", "musica_portada.mp3")
        self.musica_portada = pg.mixer.Sound(ruta_musica)

    def bucle_principal(self):
        super().bucle_principal()
        salir = False
        self.musica_portada.play()
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if self.barra_pulsada(evento):
                    self.musica_portada.fadeout(1000)
                    salir = True
            self.pantalla.blit(self.imagen, (0, 0))
            self.pintar_logo()
            self.pintar_mensaje(MENSAJE_PORTADA, 40, altura_opc=(ALTO/2) - 80)
            self.pintar_mensaje_barra()
            pg.display.flip()
        return False


class Gestion_records (Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.records = Records()
        ruta = os.path.join("resources", "images",
                            "background", "fondo_records.jpg")
        self.fondo = pg.image.load(ruta)

# Pantalla_puntos y Pantalla_records heredan de la clase Gestion_records, y asi comparten la clase Records y el fondo


class Pantalla_puntos(Gestion_records):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        alto_tipo_nombre = 80
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, alto_tipo_nombre)

        self.nombre = ""
        self.pide_nombre = True
        ruta_musica = os.path.join(
            "resources", "sounds", "musica_puntos.mp3")
        self.musica = pg.mixer.Sound(ruta_musica)

    def bucle_principal(self, puntuacion):
        super().bucle_principal()
        self.nombre = ""
        self.pide_nombre = True
        es_record = self.records.es_record(puntuacion)
        self.musica.play()
        center_nombre = (ANCHO/2, 5*(ALTO/8) + 165)
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_logo()
            if es_record:
                self.pintar_mensaje(
                    "¡Enhorabuena! Nuevo record.\nIntroduce tu nombre\n(max 10 caracteres)\ny pulsa INTRO", 45)
                if self.pide_nombre:
                    imagen_nombre = self.tipo.render(
                        self.nombre, True, COLOR_OBJETOS, (0, 0, 0))
                    self.rect_fondo = imagen_nombre.get_rect(
                        center=center_nombre)
                    self.pantalla.blit(
                        imagen_nombre, self.rect_fondo)
                    self.nombre = self.pedir_nombre()
                else:
                    if self.nombre == "":
                        nombre = "SIN NOMBRE"
                    else:
                        nombre = self.nombre
                    self.records.insertar_record(nombre, puntuacion)
                    self.musica.stop()
                    salir = True
            else:
                self.pintar_mensaje(
                    "Esta vez no has estado entre los 5 mejores.\n¡Vuelve a intentarlo!", 45)
                self.pintar_mensaje_barra()
                for evento in pg.event.get():
                    if evento.type == pg.QUIT:
                        return True
                    if self.barra_pulsada(evento):
                        self.musica.stop()
                        salir = True

            pg.display.flip()
        return False

    def pedir_nombre(self):
        for evento in pg.event.get():
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:
                    self.pide_nombre = False
                elif evento.key == pg.K_BACKSPACE:
                    self.nombre = self.nombre[:-1]
                else:
                    self.nombre += evento.unicode

                    if len(self.nombre) > 10:
                        self.nombre = self.nombre[:10]
        return self.nombre


class Pantalla_records(Gestion_records):

    def __init__(self, pantalla):
        super().__init__(pantalla)
        ruta_musica = os.path.join("resources", "sounds", "musica_records.mp3")
        self.musica = pg.mixer.Sound(ruta_musica)
        ALTO_LETRA = 30
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, ALTO_LETRA)
        self.x_nombres, self.x_puntos = self.calcular_coord_tablarecords()
        self.alto_fila_letra = ALTO_LETRA+10

    def bucle_principal(self):
        super().bucle_principal()
        self.records.actualizar()
        self.musica.play()
        salir = False

        # lanza un evento para que cuando lo lea el bucle, salte a la siguiente pantalla (empezar juego)
        pg.time.set_timer(pg.K_0, 10000)

        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if evento.type == pg.K_0 or (evento.type == pg.KEYDOWN and evento.key == pg.K_s):
                    self.musica.stop()
                    salir = True
                elif evento.type == pg.KEYDOWN and evento.key == pg.K_n:
                    return True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_logo()
            self.pintar_records()
            self.pintar_mensaje(
                "¿Juegas otra vez? (S/N)", 45, altura_opc=(3*ALTO)/4)
            pg.display.flip()
        return False

    def calcular_coord_tablarecords(self):
        puntos_max = "9999999"
        imagen_puntos_max = self.tipo.render(puntos_max, True, (0, 0, 0))
        rect_maximo_puntos = imagen_puntos_max.get_rect()
        longitud_puntos = rect_maximo_puntos.width
        nombre_max = "AAAAAAAAAA"
        imagen_nombre_max = self.tipo.render(nombre_max, True, (0, 0, 0))
        rect_nombre_max = imagen_nombre_max.get_rect()
        longitud_nombre = rect_nombre_max.width
        ancho_area_impresion = longitud_nombre + \
            (longitud_puntos + longitud_nombre/5)
        x_nombres = (ANCHO-ancho_area_impresion)/2
        x_puntos = x_nombres+ancho_area_impresion
        return x_nombres, x_puntos

    def pintar_records(self):
        linea = 0
        # imprime columna nombres:
        for dupla in self.records.lista_records:
            cadena_nombre = "{:<} ".format(dupla[0])
            cadena_puntos = "{: >7}".format(str(dupla[1]))
            texto_nombre = self.tipo.render(cadena_nombre, True, COLOR_OBJETOS)
            texto_puntos = self.tipo.render(cadena_puntos, True, COLOR_OBJETOS)
            rect_puntos = texto_puntos.get_rect()
            nombre_y = ((3*ALTO)/8) + (linea*self.alto_fila_letra)
            rect_puntos.right = self.x_puntos
            rect_puntos.y = ((3*ALTO)/8) + (linea*self.alto_fila_letra)
            linea += 1

            self.pantalla.blit(texto_nombre, (self.x_nombres, nombre_y))
            self.pantalla.blit(texto_puntos, rect_puntos)
