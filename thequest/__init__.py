# constantes de configuración de The Quest

# Relativas al display
ALTO = 720
ANCHO = 1280

ALTO_MARCADOR = 50

COLOR_OBJETOS = (255, 255, 255)

DURACION_TURNO = 500

FPS = 25

MAX_NIVELES = 3
NUM_VIDAS = 3

MARGEN_IZQ = 30
MARGEN_DCH = ANCHO-MARGEN_IZQ

# constantes para creacion de campo de asteorides:
# hay tres tipos de asteroides, 1. pequeño y rápido, 2. normal, y 3. grande y lento
TIPOS_DE_ASTEROIDES = 3
RADIO_MAX_ASTER = 45
VEL_ASTER = [10, 15, 20]
RAD_ASTER = [RADIO_MAX_ASTER, RADIO_MAX_ASTER/2, RADIO_MAX_ASTER/3]
ORIGEN_ASTER = ANCHO + RADIO_MAX_ASTER
ASTEROIDES_POR_NIVEL = [5, 10, 15]
FACTOR_PUNTOS = 1000
VEL_NAVE = 20
