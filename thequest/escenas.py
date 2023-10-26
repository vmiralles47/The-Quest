import os
from random import randint, randrange

import pygame as pg


from . import (ANCHO, ALTO, ALTO_MARCADOR, ASTEROIDES_POR_NIVEL, COLOR_OBJETOS, FACTOR_PUNTOS,
               FPS, MARGEN_IZQ, MAX_NIVELES, NUM_VIDAS, ORIGEN_ASTER, RUTA_TIPOGRAFIA,
               TIPOS_DE_ASTEROIDES, VEL_ASTER)

from .entidades import Asteroide, Contador_Vidas, Fondo, Marcador, Nave
from .records import Records


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        """
        método para ser implementado por cada escena, 
        en función de lo que estén esperando hastala condición de salida
        """

    def barra_pulsada(self, evento):
        if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
            return True

    def pintar_mensaje(self, cadena, tamanio):
        ruta = os.path.join("resources", "fonts", "Square.ttf")
        tipo = pg.font.Font(ruta, tamanio)
        mensaje = cadena
        lineas = mensaje.splitlines()
        altura = tipo.get_height()
        contador = 0
        for linea in lineas:
            texto_imagen = tipo.render(linea, True, COLOR_OBJETOS)
            x = (ANCHO-texto_imagen.get_width())/2
            y = (ALTO/2) + contador*altura
            contador += 1
            self.pantalla.blit(texto_imagen, (x, y))

    def pintar_mensaje_barra(self):
        ruta = os.path.join("resources", "fonts", "Square.ttf")
        tipo = pg.font.Font(ruta, 15)
        mensaje = "Pulsa ESPACIO para continuar"
        texto_imagen = tipo.render(mensaje, True, COLOR_OBJETOS, (0, 0, 0))
        x = (ANCHO-texto_imagen.get_width())/2
        y = 5*(ALTO/6)
        self.pantalla.blit(texto_imagen, (x, y))

    def pintar_logo(self):
        # de momenot escribe el nombre del juego con una fuente chula
        ruta = os.path.join("resources", "fonts", "spaceranger.ttf")
        tipo = pg.font.Font(ruta, 100)
        mensaje = "THE QUEST"
        texto_imagen = tipo.render(mensaje, True, COLOR_OBJETOS)
        x = (ANCHO - texto_imagen.get_width())/2
        y = (ALTO - texto_imagen.get_height())/4
        self.pantalla.blit(texto_imagen, (x, y))
# pantalla inicial con título,la historia de THE QUEST y press space to continue/puede alternar con RECORDS


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print("bucle principal de Portada")
        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    # ():
                    return True
                if self.barra_pulsada(evento):
                    salir = True
            # 2. Calcular estado de elementos y pintarlos elementos
            self.pantalla.fill((8, 50, 163))
            # pintar.logo
            self.pintar_logo()
            # pintar.backstory
            self.pintar_mensaje(
                "Explora la galaxia en busca de nuevos mundos.\nEsquiva los obstáculos, aterriza y lleva\nuna nueva esperanza a la Humanidad", 30)
            # pintar "pulsar SPACE_BAR para empezar"
            self.pintar_mensaje_barra()

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False


# pantalla donde se desarrolla cada nivel del juego. recibe como parámetro en qué nivel está para ajustar la dificultad


class Nivel(Escena):
    # atributo de clase, para que lo usen los distintos niveles
    puntuacion = 0
    vidas = NUM_VIDAS

    def __init__(self, pantalla, nivel):
        super().__init__(pantalla)
        self.nivel = nivel
        self.jugador = Nave()
        self.fondo1 = Fondo()
        self.fondo2 = Fondo()
        self.fondo2.rect.x = ANCHO+1  # se queda preparado en el limite derecho de la pantalla
        self.campo_asteroides = []

        # self.asteroide = Asteroide(ANCHO, ALTO/2, 20, 2)
        self.pantalla = pantalla
        print("Nivel.puntacion= ", Nivel.puntuacion)
        self.marcador = Marcador(Nivel.puntuacion)
        self.contador_vidas = Contador_Vidas(Nivel.vidas)
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, 60)

    def bucle_principal(self):

        super().bucle_principal()
        print("bucle principal de Juego")
        self.campo_asteroides = self.crear_campo_asteroides(self.nivel)
        salir = False
        ha_aterrizado = False
        while not salir:
            self.reloj.tick(FPS)
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if self.barra_pulsada(evento):
                    salir = True

            # self.pantalla.fill((66, 66, 66))
            self.pintar_fondo()
            if self.contador_vidas.consultar() == 0:
                subir_nivel = self.final_de_partida()
            elif self.campo_asteroides == []:
                print("lista asteroides vacía")
                self.jugador.aterriza = True
                ha_aterrizado = self.jugador.update_aterrizaje()
                self.pintar_frame_aterrizaje()
                if ha_aterrizado:
                    subir_nivel = self.resolver_final_de_nivel()
            else:
                for asteroide in self.campo_asteroides:
                    if asteroide.update(self.nivel):
                        self.marcador.incrementar(
                            asteroide.tipo*FACTOR_PUNTOS*self.nivel)
                        self.campo_asteroides.remove(asteroide)
                    elif pg.sprite.collide_rect(asteroide, self.jugador):
                        self.resolver_choque(asteroide)
                    else:
                        self.pantalla.blit(asteroide.imagen, asteroide.rect)

                if self.jugador.explota:
                    self.jugador.explota = self.pintar_explosion()
                else:
                    self.jugador.update()
                    self.pintar_nave()

            self.pintar_marcador()
            self.pintar_contador_vidas()

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        # lanzar el juego desde el nivel 1 hasta el máx niveles
        Nivel.puntuacion = self.marcador.total
        if subir_nivel:
            Nivel.vidas = self.contador_vidas.total_vidas
        return False, subir_nivel

    def crear_campo_asteroides(self, nivel):
        campo_aster = []
        lista_alturas = []
        # nivel 1 10 asteroides tipo 1, 10 asteroides tipo 2, 10 asteorides tipo 3
        for i in range(0, ASTEROIDES_POR_NIVEL[nivel-1]):
            for r in range(0, TIPOS_DE_ASTEROIDES):
                altura = Nivel.generar_altura(lista_alturas)
                asteroide = Asteroide(r+1, altura)
                campo_aster.append(asteroide)
        print("Creados ", len(campo_aster), " asteroides")
        return campo_aster

    def final_de_partida(self):

        print("te has quedado sin vidas")

        self.pintar_mensaje("no te quedan naves", 60)
        self.pintar_mensaje_barra()
        return False
        # comprobar record
        # si es record pedir datos y guardar en base de datos

    def generar_altura(lista):
        # es un método de Clase, por probar.
        # genera una pos x aleatoria entre 0 y ALTO_MARCADOR, tomada de 50 en 50 y que no puede repetirse

        altura = randrange((ALTO_MARCADOR+45),
                           ALTO)
        exit = False
        while exit == False:
            if altura in lista:
                altura = randint(0, ALTO)
            else:
                lista.append(altura)
                exit = True
        return altura

    def pintar_contador_vidas(self):
        vidas = str(self.contador_vidas.consultar())
        texto = self.tipo.render(vidas, True, COLOR_OBJETOS)
        pos_x = ANCHO - 100
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_explosion(self):

        fin_explosion = self.jugador.update_explosion()
        self.pintar_frame_explosion()
        return fin_explosion

    def pintar_fondo(self):
        if (self.fondo1.rect.right > ANCHO) and (self.fondo2.rect.left > ANCHO):
            self.fondo1.update()
            self.pantalla.blit(self.fondo1.imagen, self.fondo1.rect)
        elif (0 < self.fondo1.rect.right <= ANCHO):
            self.fondo1.update()
            self.fondo2.update()
            self.pantalla.blit(self.fondo1.imagen, self.fondo1.rect)
            self.pantalla.blit(self.fondo2.imagen, self.fondo2.rect)
            if self.fondo1.rect.right <= 0:
                self.fondo1.rect.left = ANCHO
        elif (self.fondo2.rect.right > ANCHO):
            self.fondo2.update()
            self.pantalla.blit(self.fondo2.imagen, self.fondo2.rect)

        elif (0 < self.fondo2.rect.right <= ANCHO):
            self.fondo2.update()
            self.fondo1.update()
            self.pantalla.blit(self.fondo1.imagen, self.fondo1.rect)
            self.pantalla.blit(self.fondo2.imagen, self.fondo2.rect)
            if self.fondo2.rect.right <= 0:
                self.fondo2.rect.left = ANCHO+1

    def pintar_frame_aterrizaje(self):
        print(self.jugador.rect)
        self.pantalla.blit(self.jugador.imagen,
                           self.jugador.rect)

    def pintar_frame_explosion(self):

        self.pantalla.blit(self.jugador.imagen,
                           self.jugador.rect)

        self.jugador.imagen.fill((0, 0, 0))

    def pintar_marcador(self):
        vidas = str(self.marcador.consultar())
        texto = self.tipo.render(vidas, True, COLOR_OBJETOS)
        pos_x = MARGEN_IZQ
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_nave(self):

        self.pantalla.blit(self.jugador.imagen,
                           self.jugador.rect)

    def resolver_choque(self, asteroide):
        self.contador_vidas.restar_vida()
        self.campo_asteroides.remove(asteroide)
        self.jugador.explota = True
        self.jugador.imagen.fill((0, 0, 0))

    def resolver_final_de_nivel(self):
        # self.jugador.aterrizar()
        print("self.marcador.total = ", self.marcador.total)
        print("Nivel.puntacion= ", Nivel.puntuacion)
        print("has superado el nivel")
        self.pintar_mensaje("Has superado el nivel", 60)
        self.pintar_mensaje_barra()
        return True


class Gestion_records (Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.records = Records()


class Pantalla_puntos(Gestion_records):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self, puntuacion):
        super().bucle_principal()
        print("bucle principal de Pantalla_Puntos")
        es_record = False
        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    # ():
                    return True
                if self.barra_pulsada(evento):
                    salir = True
            # 2. Calcular estado de elementos y pintarlos elementos
            self.pantalla.fill((0, 0, 99))
            self.pintar_logo()
            es_record = self.comprobar_record(puntuacion)
            pg.display.flip()
            if es_record:
                nombre = self.pedir_nombre()
                self.records.insertar_record(nombre, puntuacion)
                salir = True
            # salir = self.empezar_partida()
            # 3. Mostrar los cambios (pintados) y controlar el reloj
            # pg.display.flip()
        return False

    def comprobar_record(self, puntuacion):

        if self.records.es_record(puntuacion):
            self.pintar_mensaje(
                "has hecho nuevo record.\nintroduce tu nombre", 45)
            self.pintar_mensaje_barra()
            return True

            # pintar en pantalla "Tu puntación es de nivel.puntuacion" entras en la lista de records!"
        else:
            self.pintar_mensaje(
                "esta vez no has estado entre los 10 mejores.\nVuelve a intentarlo!!", 45)
            self.pintar_mensaje_barra()
            return False
        # pintar en pantalla " "

    def pedir_nombre(self):
        ruta = os.path.join("resources", "fonts", "Square.ttf")
        tipo = pg.font.Font(ruta, 80)
        salir = False
        nombre = ""
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_RETURN:
                        salir = True
                        return nombre
                    else:
                        nombre += evento.unicode
                        if len(nombre) > 10:
                            nombre = nombre[:10]
                        texto_imagen = tipo.render(
                            nombre, True, COLOR_OBJETOS, (0, 0, 0))
                        x = (ANCHO-texto_imagen.get_width())/2
                        y = 5*(ALTO/8) + 30

                        self.pantalla.blit(texto_imagen, (x, y))
                        pg.display.flip()


class Pantalla_records(Gestion_records):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print("bucle principal de Pantalla_Records")
        self.records.actualizar()

        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    # ():
                    return True
                if self.barra_pulsada(evento):
                    salir = True
            # 2. Calcular estado de elementos y pintarlos elementos
            self.pantalla.fill((0, 0, 99))
            self.pintar_logo()

            self.pintar_records()
            # salir = self.empezar_partida()
            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False

    def pintar_records(self):
        ruta = os.path.join("resources", "fonts", "Square.ttf")
        tipo = pg.font.Font(ruta, 30)
        l = 0
        # imprime columna nombres:
        for dupla in self.records.lista_records:
            cadena_nombre = f"{l+1} - {dupla[0]}"
            cadena_puntos = "{}".format(str(dupla[1]))
            texto_nombre = tipo.render(cadena_nombre, True, COLOR_OBJETOS)
            texto_puntos = tipo.render(cadena_puntos, True, COLOR_OBJETOS)
            nombre_x = ((3*ANCHO)/8)
            nombre_y = ((3*ALTO)/8) + (l*40)
            puntos_x = ((4*ANCHO)/7)
            puntos_y = ((3*ALTO)/8) + (l*40)
            l += 1
            self.pantalla.blit(texto_nombre, (nombre_x, nombre_y))
            self.pantalla.blit(texto_puntos, (puntos_x, puntos_y))
