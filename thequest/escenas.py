import os
from random import randint, randrange

import pygame as pg

from . import ANCHO, ALTO, ALTO_MARCADOR, COLOR_OBJETOS, MAX_NIVELES, NUM_VIDAS, ORIGEN_ASTER, RAD_ASTER, RADIO_MAX_ASTER, VEL_ASTER
from .entidades import Asteroide, Contador_Vidas, Marcador, Nave


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
            self.pintar_backstory()
            # pintar "pulsar SPACE_BAR para empezar"
            self.pintar_mensaje_barra()

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False

    def pintar_logo(self):
        # de momenot escribe el nombre del juego con una fuente chula
        ruta = os.path.join("resources", "fonts", "spaceranger.ttf")
        tipo = pg.font.Font(ruta, 100)
        mensaje = "THE QUEST"
        texto_imagen = tipo.render(mensaje, True, COLOR_OBJETOS)
        x = (ANCHO - texto_imagen.get_width())/2
        y = (ALTO - texto_imagen.get_height())/4
        self.pantalla.blit(texto_imagen, (x, y))

    def pintar_backstory(self):
        ruta = os.path.join("resources", "fonts", "Square.ttf")
        tipo = pg.font.Font(ruta, 30)
        mensaje = "Explora la galaxia en busca de nuevos mundos.\nEsquiva los obstáculos, aterriza y lleva\nuna nueva esperanza a la Humanidad"
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
# pantalla donde se desarrolla cada nivel del juego. recibe como parámetro en qué nivel está para ajustar la dificultad


class Juego(Escena):
    lista_alturas = []

    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.max_niveles = MAX_NIVELES
        self.jugador = Nave()
        self.campo_asteroides = []
        self.campo_asteroides = self.crear_campo_asteroides()
        # self.asteroide = Asteroide(ANCHO, ALTO/2, 20, 2)
        self.pantalla = pantalla
        self.marcador = Marcador()
        self.contador_vidas = Contador_Vidas(NUM_VIDAS)

    def bucle_principal(self):
        super().bucle_principal()
        print("bucle principal de Juego")
        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if self.barra_pulsada(evento):
                    salir = True

            self.pantalla.fill((66, 66, 66))

            self.jugador.update()
            self.pintar_nave()
            self.marcador.pintar(self.pantalla)
            self.contador_vidas.pintar(self.pantalla)

            if self.contador_vidas.consultar() == 0:
                self.final_de_partida()
                salir = True

            else:
                for asteroide in self.campo_asteroides:
                    eliminado = asteroide.update()
                    asteroide.pintar(self.pantalla)
                    if pg.Rect.colliderect(asteroide.rect, self.jugador.rect):
                        self.resolver_choque(asteroide)

                    if eliminado:
                        self.marcador.incrementar(asteroide.tipo*10)
                        print("asteroide eliminado tipo ", asteroide.tipo)
                        self.campo_asteroides.remove(asteroide)

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        # lanzar el juego desde el nivel 1 hasta el máx niveles
        return False

    def final_de_partida(self):
        print("te has quedado sin vidas")
        # comprobar record
        # si es record pedir datos y guardar en base de datos

    def resolver_choque(self, asteroide):
        print("colisión")
        self.contador_vidas.restar_vida()
        self.campo_asteroides.remove(asteroide)
        self.jugador.explotar()
        for ast in self.campo_asteroides:
            ast.turno += 200

        # cómo paro la partida?

    def pintar_nave(self):
        self.pantalla.blit(self.jugador.imagen_nave, self.jugador.rect)

    def crear_campo_asteroides(self):
        campo_aster = []
        # nivel 1 10 asteroides tipo 1, 10 asteroides tipo 2, 10 asteorides tipo 3
        for i in range(0, 10):
            for r in range(0, MAX_NIVELES):
                altura = self.generar_altura()
                asteroide = Asteroide(r+1, ORIGEN_ASTER, altura,
                                      RAD_ASTER[r], VEL_ASTER[r])
                print("asteroide tipo ", r+1, "turno = ", asteroide.turno,
                      "radio ", asteroide.radio, "velocidad ", asteroide.velocidad, "altura ", asteroide.pos_y)
                campo_aster.append(asteroide)
        return campo_aster

    def generar_altura(self):
        # genera una pos x aleatoria entre 0 y ALTO, tomada de 50 en 50 y que no puede repetirse
        altura = randrange((ALTO_MARCADOR+RADIO_MAX_ASTER),
                           ALTO)
        exit = False
        while exit == False:
            if altura in self.lista_alturas:
                altura = randint(0, ALTO)
            else:
                self.lista_alturas.append(altura)
                exit = True
        return altura

    def muestra_mensaje(self,cadena):
        
class Records(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

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

            # salir = self.empezar_partida()
            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False
