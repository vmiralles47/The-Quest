# constantes de configuración de The Quest
import os

# Relativas al display

fuente = "Square.ttf"
RUTA_TIPOGRAFIA = os.path.join("resources", "fonts", fuente)
MENSAJE_PORTADA = "Explora la galaxia en busca de nuevos mundos.\nEsquiva los obstáculos, aterriza y lleva\nuna nueva esperanza a la Humanidad.\n\nMueve la nave con las teclas\nflecha arriba y flecha abajo."

ALTO = 720
ANCHO = 1280
ALTO_MARCADOR = 50

COLOR_OBJETOS = (255, 255, 255)

DURACION_TURNO = 500  # RESTAURAR

FPS = 15

MAX_NIVELES = 4
MAX_RECORDS = 5
NUM_VIDAS = 3

MARGEN_IZQ = 30
MARGEN_DCH = ANCHO-MARGEN_IZQ

# constantes para creacion de campo de asteorides:
# hay tres tipos de asteroides, 1. pequeño y rápido, 2. normal, y 3. grande y lento
TIPOS_DE_ASTEROIDES = 3

VEL_ASTER = [15, 12, 10]

ORIGEN_ASTER = ANCHO + 45  # OJO NUMERO MAGICO
ASTEROIDES_POR_NIVEL = [3, 30, 30, 40]
# aSTEROIDES_POR_NIVEL = [1, 2, 3, 4] para pruebas
FACTOR_PUNTOS = 1000  # RESTAURAR
PUNTOS_POR_PLANETA = 5000
VEL_NAVE = 25
VEL_FACTOR_INERCIA = 3
VEL_MAX_NAVE = 100

VEL_PLANETA = 10
