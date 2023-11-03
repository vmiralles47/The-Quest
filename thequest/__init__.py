# constantes de configuración de The Quest
import os

# Relativas al display

FUENTE = "Square.ttf"
RUTA_TIPOGRAFIA = os.path.join("resources", "fonts", FUENTE)
MENSAJE_PORTADA = "Explora la galaxia en busca de nuevos mundos.\nEsquiva los obstáculos, aterriza y lleva\nuna nueva esperanza a la Humanidad.\n\nMueve la nave con las teclas\nflecha arriba y flecha abajo."

ALTO = 720
ANCHO = 1280
ALTO_MARCADOR = 50

COLOR_OBJETOS = (255, 255, 255)

DURACION_TURNO = 850  # RESTAURAR

FPS = 16

MAX_NIVELES = 4
MAX_RECORDS = 5
NUM_VIDAS = 3

MARGEN_IZQ = 30
MARGEN_DCH = ANCHO-MARGEN_IZQ

# constantes para creacion de campo de asteorides:
# hay tres tipos de asteroides, 1 - grande y lento, 2 - normal, y 3 -  pequeño y rápido
TIPOS_DE_ASTEROIDES = 3

VEL_ASTER = [10, 15, 20]

ORIGEN_ASTER = ANCHO + 45  # OJO NUMERO MAGICO
ASTEROIDES_POR_NIVEL = [10, 20, 30, 40]  # creara estos x cada tipo
# aSTEROIDES_POR_NIVEL = [1, 2, 3, 4] para pruebas
FACTOR_PUNTOS = 100  # RESTAURAR
PUNTOS_POR_PLANETA = 5000

VEL_NAVE = 8
VEL_FACTOR_INERCIA = 5
VEL_MAX_NAVE = 80

VEL_PLANETA = 8
