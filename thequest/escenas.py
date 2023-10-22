import os
from random import randint, randrange

import pygame as pg

from . import (ANCHO, ALTO, ALTO_MARCADOR, ASTEROIDES_POR_NIVEL, COLOR_OBJETOS,
               FPS, MAX_NIVELES, NUM_VIDAS, ORIGEN_ASTER, RAD_ASTER, RADIO_MAX_ASTER,
               TIPOS_DE_ASTEROIDES, VEL_ASTER)

from .entidades import Asteroide, Contador_Vidas, Marcador, Nave
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

    def pintar_mensaje(self, cadena):
        ruta = os.path.join("resources", "fonts", "Square.ttf")
        tipo = pg.font.Font(ruta, 30)
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
                "Explora la galaxia en busca de nuevos mundos.\nEsquiva los obstáculos, aterriza y lleva\nuna nueva esperanza a la Humanidad")
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
        self.campo_asteroides = []

        # self.asteroide = Asteroide(ANCHO, ALTO/2, 20, 2)
        self.pantalla = pantalla
        print("Nivel.puntacion= ", Nivel.puntuacion)
        self.marcador = Marcador(Nivel.puntuacion)
        self.contador_vidas = Contador_Vidas(Nivel.vidas)

    def bucle_principal(self):

        super().bucle_principal()
        print("bucle principal de Juego")
        self.campo_asteroides = self.crear_campo_asteroides(self.nivel)

        salir = False
        while not salir:
            self.reloj.tick(FPS)
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if self.barra_pulsada(evento):
                    salir = True

            self.pantalla.fill((66, 66, 66))
            self.jugador.update()
            self.pintar_nave()

            if self.contador_vidas.consultar() == 0:
                subir_nivel = self.final_de_partida()

            elif self.campo_asteroides == []:
                subir_nivel = self.final_de_nivel()
            else:
                for asteroide in self.campo_asteroides:
                    eliminado = asteroide.update(self.nivel)
                    asteroide.pintar(self.pantalla)
                    if pg.Rect.colliderect(asteroide.rect, self.jugador.rect):
                        self.resolver_choque(asteroide)
                    if eliminado:
                        self.marcador.incrementar(asteroide.tipo*10*self.nivel)
                        print("asteroide eliminado tipo ", asteroide.tipo)
                        self.campo_asteroides.remove(asteroide)

            self.marcador.pintar(self.pantalla)
            self.contador_vidas.pintar(self.pantalla)

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        # lanzar el juego desde el nivel 1 hasta el máx niveles
        if subir_nivel:
            Nivel.puntuacion = self.marcador.total
            Nivel.vidas = self.contador_vidas.total_vidas
        return False, subir_nivel

    def final_de_nivel(self):
        print("self.marcador.total = ", self.marcador.total)

        print("Nivel.punutacion= ", Nivel.puntuacion)
        print("has superado el nivel")
        self.pintar_mensaje("Has superado el nivel")
        self.pintar_mensaje_barra()
        return True

    def final_de_partida(self):

        print("te has quedado sin vidas")

        self.pintar_mensaje("has perdido")
        self.pintar_mensaje_barra()
        return False
        # comprobar record
        # si es record pedir datos y guardar en base de datos

    def resolver_choque(self, asteroide):
        print("colisión")
        self.contador_vidas.restar_vida()
        self.campo_asteroides.remove(asteroide)
        self.jugador.explotar()
        # cómo paro la partida?
        pg.time.delay(1000)
        """
        for ast in self.campo_asteroides:
            ast.turno += 200
        """

    def pintar_nave(self):
        self.pantalla.blit(self.jugador.imagen_nave, self.jugador.rect)

    def crear_campo_asteroides(self, nivel):
        campo_aster = []
        lista_alturas = []
        # nivel 1 10 asteroides tipo 1, 10 asteroides tipo 2, 10 asteorides tipo 3
        for i in range(0, ASTEROIDES_POR_NIVEL[nivel-1]):
            for r in range(0, TIPOS_DE_ASTEROIDES):
                altura = Nivel.generar_altura(lista_alturas)
                asteroide = Asteroide(r+1, altura)
                campo_aster.append(asteroide)
        print("Creados ", len(campo_aster), " asteorides")
        return campo_aster

    def generar_altura(lista):
        # es un método de Clase, por probar.
        # genera una pos x aleatoria entre 0 y ALTO, tomada de 50 en 50 y que no puede repetirse

        altura = randrange((ALTO_MARCADOR+RADIO_MAX_ASTER),
                           ALTO)
        exit = False
        while exit == False:
            if altura in lista:
                altura = randint(0, ALTO)
            else:
                lista.append(altura)
                exit = True
        return altura


class Pantalla_records(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.records = Records()

    def bucle_principal(self):
        super().bucle_principal()
        print("bucle principal de Records")
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
        for dupla in self.records.lista_records:
            linea = f"{dupla[0]} ------- {str(dupla[1])}"
            texto = tipo.render(linea, True, (230, 189, 40))
            pos_x = (500)
            pos_y = (ALTO/2) + (l*40)
            l += 1
            self.pantalla.blit(texto, (pos_x, pos_y))
