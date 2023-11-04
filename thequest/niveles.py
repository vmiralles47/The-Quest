import os
from random import randrange

import pygame as pg


from . import (ANCHO, ALTO, ALTO_MARCADOR, ASTEROIDES_POR_NIVEL, COLOR_OBJETOS, DURACION_TURNO,
               FACTOR_PUNTOS, FPS, MARGEN_IZQ, MAX_NIVELES, NUM_VIDAS,
               PUNTOS_POR_PLANETA, RUTA_TIPOGRAFIA, TIPOS_DE_ASTEROIDES, VEL_NAVE)

from .escenas import Escena
from .entidades import Asteroide, Contador_Niveles, Contador_Vidas, Fondo, Marcador, Nave, Planeta


# Nivel es la antalla donde se desarrolla cada nivel del juego.
# Recibe como parámetro en qué nivel está para ajustar la dificultad

class Nivel(Escena):
    # atributo de clase, para que lo usen los distintos niveles
    puntuacion = 0
    vidas = NUM_VIDAS

    def __init__(self, pantalla, nivel):
        super().__init__(pantalla)
        self.pantalla = pantalla
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
        ruta_musica = os.path.join(
            "resources", "sounds", "musica_nonaves.mp3")
        self.musica_nonaves = pg.mixer.Sound(ruta_musica)

        if nivel == 1:
            Nivel.puntuacion = 0
            Nivel.vidas = NUM_VIDAS

        self.marcador = Marcador(Nivel.puntuacion)
        self.contador_niveles = Contador_Niveles(MAX_NIVELES)
        self.contador_vidas = Contador_Vidas(Nivel.vidas)
        self.tipo = pg.font.Font(RUTA_TIPOGRAFIA, 60)

    def bucle_principal(self):
        super().bucle_principal()
        self.campo_asteroides = self.crear_campo_asteroides(self.nivel)
        salir = False
        esperando_barra = False
        preparado_para_rotar = False
        ha_aterrizado = False
        x_aterrizaje = ANCHO
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return True
                if esperando_barra:
                    if evento.type == pg.KEYDOWN and evento.key == pg.K_SPACE:
                        salir = True

            self.pintar_fondo()
            if self.contador_vidas.consultar() == 0:
                self.resolver_final_de_partida()
                esperando_barra = True
                if salir:
                    self.musica_nonaves.stop()

            elif self.flag_fin_de_nivel:  # se acaba el nivel
                self.pintar_planeta()
                if not preparado_para_rotar:
                    preparado_para_rotar = (
                        self.jugador.update_va_al_centro() and
                        self.planeta.rect.centerx <= ANCHO)
                    self.pintar_nave()
                    # mientras va al centro para comenzar la rotacion, sale el planeta
                    # la coord de aterrizaje depende de las dimensiones del planeta
                    x_aterrizaje = self.planeta.update()
                    # en el planeta del nivel extra pasa algo distinto
                    if self.nivel == 4:
                        self.planeta.play_music_nivel4()

                elif not ha_aterrizado:
                    ha_aterrizado = self.jugador.update_rotacion(x_aterrizaje)

                else:  # ya ha aterrizado
                    self.resolver_final_de_nivel()
                    esperando_barra = True
                    if salir:
                        if self.nivel == 4:
                            self.planeta.musica_nivel4.stop()
                        else:
                            self.musica_findenivel.fadeout(500)
                self.pintar_nave_rotando()
            else:
                for asteroide in self.campo_asteroides:
                    sale = asteroide.update(self.nivel)
                    choca = pg.sprite.collide_rect(
                        asteroide, self.jugador)
                    if sale or choca:
                        self.campo_asteroides.remove(asteroide)
                        if sale:
                            self.marcador.incrementar(
                                asteroide.tipo*FACTOR_PUNTOS*self.nivel)
                        if choca:
                            self.resolver_choque()
                            if not self.flag_fin_de_nivel:
                                for asteroide in self.campo_asteroides:
                                    asteroide.rect.x += ANCHO
                        if self.campo_asteroides == [] and self.contador_vidas.consultar() > 0:
                            self.flag_fin_de_nivel = True
                            if self.nivel != 4:
                                self.musica_findenivel.play()
                            self.jugador.sonido_reactor.stop()
                            self.jugador.sonido_reactor_on = False
                    else:
                        self.pantalla.blit(asteroide.imagen, asteroide.rect)

                if self.jugador.explota:
                    self.jugador.explota = self.jugador.update_explosion()
                    self.jugador.rect_aux.center = self.jugador.rect.center
                    self.pantalla.blit(self.jugador.imagen_aux,
                                       self.jugador.rect_aux)
                    self.jugador.imagen_aux.fill((0, 0, 0))

                else:
                    if not self.flag_fin_de_nivel and not self.jugador.sonido_reactor_on:
                        self.jugador.sonido_reactor.play()
                        self.jugador.sonido_reactor_on = True
                    se_mueve = self.jugador.update()
                    if not se_mueve:
                        self.jugador.velocidad = VEL_NAVE  # resetea la velocidad inercial

                    self.pintar_nave()

            self.pintar_marcador()
            self.pintar_contador_niveles()
            self.pintar_contador_vidas()
            pg.display.flip()

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
        return campo_aster  # devuelve una lista de asteroides instancias de entidad Asteroide

    def generar_altura(lista):
        # es un método de Clase, por probar.
        # genera una pos x aleatoria entre 0 y ALTO_MARCADOR que no puede repetirse
        altura = randrange((ALTO_MARCADOR+45), ALTO, 25)
        exit = False
        while exit == False:
            if altura in lista:
                altura = randrange((ALTO_MARCADOR+45),
                                   ALTO)
            else:
                lista.append(altura)
                exit = True
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

    def pintar_fondo(self):  # pone en bucle dos copias del fondo para hacer un efecto sinfín
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

    def pintar_marcador(self):
        vidas = str(self.marcador.consultar())
        texto = self.tipo.render(vidas, True, COLOR_OBJETOS)
        pos_x = MARGEN_IZQ
        pos_y = (ALTO_MARCADOR - self.tipo.get_height())/2
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_nave(self):
        self.pantalla.blit(self.jugador.imagen_nave,
                           self.jugador.rect)

    def pintar_nave_rotando(self):

        self.pantalla.blit(self.jugador.imagen_aux,
                           self.jugador.rect_aux)
        pg.time.delay(30)  # para apreciar la explosion

    def pintar_planeta(self):
        self.pantalla.blit(self.planeta.imagen,
                           self.planeta.rect)

    def resolver_choque(self):
        self.jugador.sonido_explosion.play()
        self.jugador.sonido_reactor.stop()
        self.jugador.sonido_reactor_on = False

        self.jugador.explota = True
        self.jugador.imagen_nave.fill((0, 0, 0))
        self.contador_vidas.restar_vida()

    def resolver_final_de_nivel(self):
        if self.nivel == 4:
            self.pintar_mensaje("¡Enhorabuena,\nhas terminado el juego!", 60)
        else:
            self.pintar_mensaje(
                "Has superado el nivel {}".format(self.nivel), 60)
        self.pintar_mensaje_barra()
        self.subir_nivel = True
        if not self.asignados_puntos_nivel:
            self.marcador.incrementar(PUNTOS_POR_PLANETA)
            self.asignados_puntos_nivel = True

    def resolver_final_de_partida(self):
        self.musica_nonaves.play()
        self.pintar_mensaje("¡Has perdido todas tus naves!", 60)
        self.pintar_mensaje_barra()
        return False
