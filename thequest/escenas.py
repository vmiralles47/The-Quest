import pygame as pg
from . import ANCHO, ALTO, MAX_NIVELES


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
            self.pantalla.fill((99, 0, 0))
            # pintar.logo
            # pintar.backstory
            # pintar "pulsar SPACE_BAR para empezar"

            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False

# pantalla donde se desarrolla cada nivel del juego. recibe como parámetro en qué nivel está para ajustar la dificultad


class Nivel(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self, nivel):
        print("empieza nivel: ", nivel)
        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if self.barra_pulsada(evento):
                    salir = True
            self.pantalla.fill((nivel*60, 99, nivel*60))
            pg.display.flip()
        return False


class Juego(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.nivel = Nivel(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print("bucle principal de Juego")
        salir = False
        while not salir:
            # 1 capturar los eventos
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    # ():
                    return True
            # 2 lanzar el juego desde el nivel 1 hasta el máx niveles
            for n in range(1, MAX_NIVELES+1):
                self.nivel.bucle_principal(n)
                if n == MAX_NIVELES:
                    salir = True

            print("fin del juego pasamos a pantalla de records. PULSA BARRA")
            # 3. Mostrar los cambios (pintados) y controlar el reloj
            pg.display.flip()
        return False


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
