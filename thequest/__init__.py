# constantes de configuración de The Quest
import os

# Relativas al display

fuente = "Square.ttf"
RUTA_TIPOGRAFIA = os.path.join("resources", "fonts", fuente)

ALTO = 720
ANCHO = 1280

ALTO_MARCADOR = 50

MAX_RECORDS = 5

COLOR_OBJETOS = (255, 255, 255)

DURACION_TURNO = 50  # RESTAURAR

FPS = 15

MAX_NIVELES = 4
NUM_VIDAS = 30  # RESTAURAR

MARGEN_IZQ = 30
MARGEN_DCH = ANCHO-MARGEN_IZQ

# constantes para creacion de campo de asteorides:
# hay tres tipos de asteroides, 1. pequeño y rápido, 2. normal, y 3. grande y lento
TIPOS_DE_ASTEROIDES = 3

VEL_ASTER = [20, 15, 10]

ORIGEN_ASTER = ANCHO + 45  # OJO NUMERO MAGICO
# ASTEROIDES_POR_NIVEL = [1, 10, 15, 20]  # RESTAURAR
ASTEROIDES_POR_NIVEL = [1, 2, 3, 4]
FACTOR_PUNTOS = 100
VEL_NAVE = 20

VEL_PLANETA = 10
