import os
from random import randint, randrange

import pygame as pg


from . import (ANCHO, ALTO, ALTO_MARCADOR, ASTEROIDES_POR_NIVEL, COLOR_OBJETOS, DURACION_TURNO,
               FACTOR_PUNTOS, FPS, MARGEN_IZQ, MAX_NIVELES, MENSAJE_PORTADA, NUM_VIDAS, ORIGEN_ASTER,
               PUNTOS_POR_PLANETA, RUTA_TIPOGRAFIA, TIPOS_DE_ASTEROIDES, VEL_NAVE)

from .entidades import Asteroide, Contador_Niveles, Contador_Vidas, Fondo, Marcador, Nave, Planeta
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
        # de momenot escribe el nombre del juego con una fuente chula

        tipo = pg.font.Font(RUTA_TIPOGRAFIA, 100)
        mensaje = "THE QUEST"
        texto_imagen = tipo.render(mensaje, True, COLOR_OBJETOS)
        x = (ANCHO - texto_imagen.get_width())/2
        y = (ALTO - texto_imagen.get_height())/4
        self.pantalla.blit(texto_imagen, (x, y))
        # pantalla inicial con título,la historia de THE QUEST y press space to continue/puede alternar con RECORDS


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
        print("bucle principal de Portada")
        salir = False
        self.musica_portada.play()
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:

                    return True
                if self.barra_pulsada(evento):
                    self.musica_portada.fadeout(1000)
                    salir = True
            # 2. Calcular estado de elementos y pintarlos elementos
            # self.pantalla.fill((8, 50, 163))
            self.pantalla.blit(self.imagen, (0, 0))
            # pintar.logo
            self.pintar_logo()
            # pintar.backstory
            self.pintar_mensaje(MENSAJE_PORTADA, 40, altura_opc=(ALTO/2) - 80)
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
        self.subir_nivel = False
        self.flag_fin_de_nivel = False
        self.asignados_puntos_nivel = False
        self.jugador = Nave()
        self.fondo1 = Fondo()
        self.fondo2 = Fondo()
        self.fondo2.rect.x = ANCHO+1  # se queda preparado en el limite derecho de la pantalla
        self.campo_asteroides = []
        self.planeta = Planeta(self.nivel)
        ruta_musica = os.path.join(
            "resources", "sounds", "musica_findenivel.mp3")
        self.musica_findenivel = pg.mixer.Sound(ruta_musica)

        # self.asteroide = Asteroide(ANCHO, ALTO/2, 20, 2)
        self.pantalla = pantalla
        if nivel == 1:
            Nivel.puntuacion = 0
            Nivel.vidas = NUM_VIDAS
        print("Nivel.puntacion= ", Nivel.puntuacion)
        self.marcador = Marcador(Nivel.puntuacion)
        self.contador_niveles = Contador_Niveles(MAX_NIVELES)
        self.contador_vidas = Contador_Vidas(Nivel.vidas)
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, 60)

    def bucle_principal(self):

        super().bucle_principal()
        print("bucle principal de Juego")
        self.campo_asteroides = self.crear_campo_asteroides(self.nivel)
        salir = False
        espera_barra = False
        preparado_para_rotar = False
        ha_aterrizado = False
        x_aterrizaje = ANCHO
        while not salir:
            self.reloj.tick(FPS)
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if espera_barra:
                    if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                        salir = True
            # self.pantalla.fill((66, 66, 66))
            self.pintar_fondo()

            if self.contador_vidas.consultar() == 0:
                self.final_de_partida()
                espera_barra = True

            elif self.flag_fin_de_nivel:  # se acaba el nivel
                if not preparado_para_rotar:
                    preparado_para_rotar = (
                        self.jugador.update_va_al_centro() and
                        self.planeta.rect.centerx <= ANCHO)
                    self.pintar_nave()
                    # mientras va al centro para comenzar la rotacion, sale el planeta
                    # la coord de aterrizaje depende de las dimensiones del planeta
                    x_aterrizaje = self.planeta.update()
                    self.pintar_planeta()
                    # en el planeta del nivel extra pasa algo especial
                    if self.nivel == 4:
                        self.planeta.play_music_nivel4()
                elif not ha_aterrizado:
                    ha_aterrizado = self.jugador.update_rotacion(x_aterrizaje)
                    self.pintar_planeta()
                    self.pintar_nave_rotando()
                else:  # ya ha aterrizado
                    self.pintar_planeta()
                    self.pintar_nave_rotando()
                    self.resolver_final_de_nivel()
                    espera_barra = True
                    if salir:
                        if self.nivel == 4:
                            self.planeta.musica_nivel4.stop()
                        else:
                            self.musica_findenivel.fadeout(500)
            else:
                for asteroide in self.campo_asteroides:
                    sale = asteroide.update(self.nivel)
                    choca = pg.sprite.collide_rect(asteroide, self.jugador)
                    if sale or choca:
                        self.campo_asteroides.remove(asteroide)

                        if sale:
                            self.marcador.incrementar(
                                asteroide.tipo*FACTOR_PUNTOS*self.nivel)

                        if choca:
                            # self.resolver_choque(asteroide)

                            self.jugador.sonido_explosion.play()
                            self.jugador.sonido_reactor.stop()
                            self.jugador.sonido_reactor_on = False
                            self.contador_vidas.restar_vida()
                            if not self.flag_fin_de_nivel:
                                for asteroide in self.campo_asteroides:
                                    asteroide.rect.x += ORIGEN_ASTER
                            self.jugador.explota = True
                            self.jugador.imagen.fill((0, 0, 0))

                        if self.campo_asteroides == [] and self.contador_vidas.consultar() > 0:
                            print("lista asteroides vacía")
                            self.flag_fin_de_nivel = True
                            if self.nivel != 4:
                                self.musica_findenivel.play()
                            self.jugador.sonido_reactor.stop()
                            self.jugador.sonido_reactor_on = False
                    else:
                        self.pantalla.blit(asteroide.imagen, asteroide.rect)

                if self.jugador.explota:
                    self.jugador.explota = self.jugador.update_explosion()
                    self.pintar_nave()
                    self.jugador.imagen.fill((0, 0, 0))

                else:
                    se_mueve = self.jugador.update()
                    if not se_mueve:
                        self.jugador.velocidad = VEL_NAVE
                    if not self.flag_fin_de_nivel:
                        if not self.jugador.sonido_reactor_on:
                            self.jugador.sonido_reactor.play()
                            self.jugador.sonido_reactor_on = True
                    self.pintar_nave()

            self.pintar_marcador()
            self.pintar_contador_niveles()
            self.pintar_contador_vidas()

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        # lanzar el juego desde el nivel 1 hasta el máx niveles
        Nivel.puntuacion = self.marcador.total
        if self.subir_nivel:
            Nivel.vidas = self.contador_vidas.total_vidas
        return False, self.subir_nivel

    def crear_campo_asteroides(self, nivel):
        campo_aster = []
        lista_alturas = []
        lista_turnos = []
        # nivel 1 10 asteroides tipo 1, 10 asteroides tipo 2, 10 asteorides tipo 3
        for i in range(0, ASTEROIDES_POR_NIVEL[nivel-1]):
            for r in range(0, TIPOS_DE_ASTEROIDES):
                altura = Nivel.generar_altura(lista_alturas)
                turno = Nivel.generar_turno(lista_turnos)

                asteroide = Asteroide(altura, r+1, turno)
                campo_aster.append(asteroide)

        print("Creados ", len(campo_aster), " asteroides")
        print("lista alturas:", lista_alturas)
        print("lista turnos : ", lista_turnos)
        return campo_aster  # devuelve una lista de asteroides instancias de entidad Asteroide

    def final_de_partida(self):

        print("te has quedado sin vidas")

        self.pintar_mensaje("no te quedan naves", 60)
        self.pintar_mensaje_barra()
        print("esperando evento barra")

        return False
        # comprobar record
        # si es record pedir datos y guardar en base de datos

    def generar_altura(lista):
        # es un método de Clase, por probar.
        # genera una pos x aleatoria entre 0 y ALTO_MARCADOR, tomada de 50 en 50 y que no puede repetirse

        altura = randrange((ALTO_MARCADOR+45),
                           ALTO, 25)
        exit = False
        while exit == False:
            if altura in lista:
                altura = randrange((ALTO_MARCADOR+45),
                                   ALTO)
            else:
                lista.append(altura)
                exit = True
        print(lista)
        return altura

    def generar_turno(lista_turnos):
        turno = randrange(0, DURACION_TURNO, 25)

        exit = False
        while exit == False:
            if turno in lista_turnos:
                turno = randrange(0, DURACION_TURNO)
            else:
                lista_turnos.append(turno)
                exit = True
        print("turnos ", lista_turnos)
        return turno

    def pintar_contador_niveles(self):
        texto_nivel = f"NIVEL {str(self.nivel)}"
        texto = self.tipo.render(texto_nivel, True, COLOR_OBJETOS)
        pos_x = ANCHO - 500
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_contador_vidas(self):
        vidas = str(self.contador_vidas.consultar())
        texto = self.tipo.render(vidas, True, COLOR_OBJETOS)
        pos_x = ANCHO - 100
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        self.pantalla.blit(texto, (pos_x, pos_y))

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

    # def pintar_frame_explosion(self):

    def pintar_marcador(self):
        vidas = str(self.marcador.consultar())
        texto = self.tipo.render(vidas, True, COLOR_OBJETOS)
        pos_x = MARGEN_IZQ
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_nave(self):

        self.pantalla.blit(self.jugador.imagen,
                           self.jugador.rect)

    def pintar_nave_rotando(self):

        self.pantalla.blit(self.jugador.imagen_aux,
                           self.jugador.rect_aux)
        pg.time.delay(30)

    def pintar_planeta(self):
        self.pantalla.blit(self.planeta.imagen,
                           self.planeta.rect)

    def resolver_final_de_nivel(self):

        # self.jugador.aterrizar()
        print("self.marcador.total = ", self.marcador.total)
        print("Nivel.puntacion= ", Nivel.puntuacion)
        print("has superado el nivel", self.nivel)
        if self.nivel == 4:
            self.pintar_mensaje("¡Enhorabuena, has terminado el juego!")
        else:
            self.pintar_mensaje(
                "Has superado el nivel {}".format(self.nivel), 60)
        self.pintar_mensaje_barra()
        self.subir_nivel = True
        if not self.asignados_puntos_nivel:
            self.marcador.incrementar(PUNTOS_POR_PLANETA)
            self.asignados_puntos_nivel = True
        print("esperando evento barra")


class Gestion_records (Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.records = Records()
        ruta = os.path.join("resources", "images",
                            "background", "fondo_records.jpg")
        self.fondo = pg.image.load(ruta)


class Pantalla_puntos(Gestion_records):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        alto_tipo_nombre = 80
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, alto_tipo_nombre)
        # me hace falta un fondo negro sobre el que escribir para que funcione bien el borrado de letras
        self.nombre = ""  # un caracter ancho cualquiera
        self.pide_nombre = True

    def bucle_principal(self, puntuacion):
        super().bucle_principal()
        print("bucle principal de Pantalla_Puntos")
        es_record = self.records.es_record(puntuacion)
        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_logo()
            if es_record:
                self.pintar_mensaje(
                    "has hecho nuevo record.\nintroduce tu nombre\ny pulsa INTRO", 45)
                if self.pide_nombre:
                    imagen_nombre = self.tipo.render(
                        self.nombre, True, COLOR_OBJETOS, (0, 0, 0))
                    self.rect_fondo = imagen_nombre.get_rect(
                        center=(ANCHO/2, 5*(ALTO/8) + 120))
                    self.pantalla.blit(
                        imagen_nombre, self.rect_fondo)
                    self.nombre = self.pedir_nombre()
                    print(self.nombre, len(self.nombre))
                else:
                    nombre = self.nombre  # [:-1]
                    self.records.insertar_record(nombre, puntuacion)
                    salir = True
            else:
                self.pintar_mensaje(
                    "esta vez no has estado entre los 10 mejores.\nVuelve a intentarlo!!", 45)
                self.pintar_mensaje_barra()
                for evento in pg.event.get():
                    if evento.type == pg.QUIT:
                        return True
                    if self.barra_pulsada(evento):
                        salir = True
            # salir = self.empezar_partida()
            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False

    def pedir_nombre(self):
        for evento in pg.event.get():
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:

                    self.pide_nombre = False
                if evento.key == pg.K_BACKSPACE:
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

        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, 30)
        self.x_nombres, self.x_puntos = self.calcular_coord_tablarecords()

    def bucle_principal(self):
        super().bucle_principal()
        print("bucle principal de Pantalla_Records")
        self.records.actualizar()
        self.musica.play()
        salir = False
        a_portada = True
        pg.time.set_timer(pg.K_0, 60000)
        # pg.time.set_timer(pg.K_s, 3000)
        while not salir:
            # 1 capturar los eventos

            for evento in pg.event.get():

                if evento.type == pg.QUIT:
                    # ():
                    return True
                if evento.type == pg.K_0 or (evento.type == pg.KEYDOWN and evento.key == pg.K_s):
                    self.musica.stop()
                    salir = True
                elif evento.type == pg.KEYDOWN and evento.key == pg.K_n:
                    return True
            # 2. Calcular estado de elementos y pintarlos elementos
            # self.pantalla.fill((0, 0, 99))
            self.pantalla.blit(self.fondo, (0, 0))
            self.pintar_logo()

            self.pintar_records()
            # salir = self.empezar_partida()
            self.pintar_mensaje(
                "¿Juegas otra vez? (S/N)", 45, altura_opc=(3*ALTO)/4)

            # 3. Mostrar los cambios (pintados) y controlar el reloj
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
            # nombre_x = ((3*ANCHO)/8)
            nombre_y = ((3*ALTO)/8) + (linea*40)
            rect_puntos.right = self.x_puntos
            rect_puntos.y = ((3*ALTO)/8) + (linea*40)
            linea += 1

            self.pantalla.blit(texto_nombre, (self.x_nombres, nombre_y))
            self.pantalla.blit(texto_puntos, rect_puntos)
