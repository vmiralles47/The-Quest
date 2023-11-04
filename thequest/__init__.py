# constantes de configuración de The Quest
import os

# Relativas al display

FUENTE = "Square.ttf"
RUTA_TIPOGRAFIA = os.path.join("resources", "fonts", FUENTE)
MENSAJE_PORTADA = "Explora la galaxia en busca de nuevos mundos.\nEsquiva los obstáculos, aterriza y lleva\nuna nueva esperanza a la Humanidad.\n\nMueve la nave con las teclas\nflecha arriba y flecha abajo."

ALTO = 720
ANCHO = 1280
ALTO_MARCADOR = 50
MARGEN_IZQ = 30
MARGEN_DCH = ANCHO-MARGEN_IZQ

COLOR_OBJETOS = (255, 255, 255)

DURACION_TURNO = 100
FPS = 16

MAX_NIVELES = 4
MAX_RECORDS = 5
NUM_VIDAS = 3

# hay tres tipos de asteroides, 1 - grande y lento, 2 - normal, y 3 -  pequeño y rápido
TIPOS_DE_ASTEROIDES = 3

VEL_ASTER = [8, 12, 16]

ORIGEN_ASTER = ANCHO + 45  # OJO NUMERO MAGICO
# ASTEROIDES_POR_NIVEL = [8, 16, 24, 32]  # creara estos x cada tipo
ASTEROIDES_POR_NIVEL = [1, 2, 3, 4]
FACTOR_PUNTOS = 100
PUNTOS_POR_PLANETA = 5000

VEL_NAVE = 8
VEL_FACTOR_INERCIA = 4
VEL_MAX_NAVE = 80

VEL_PLANETA = 8
