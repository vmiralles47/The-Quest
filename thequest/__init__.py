# constantes de configuración de The Quest

# Relativas al display
ALTO = 720
ANCHO = 1280

COLOR_OBJETOS = (255, 255, 255)

DURACION_TURNO = 2000

MAX_NIVELES = 3

MARGEN_IZQ = 30
MARGEN_DCH = ANCHO-MARGEN_IZQ

# constantes para creacion de campo de asteorides:
# hay tres tipos de asteroides, 1. pequeño y rápido, 2. normal, y 3. grande y lento
VEL_ASTER = [3, 4, 5]
RAD_ASTER = [45, 30, 15]
ORIGEN_ASTER = ANCHO + RAD_ASTER[0]+10


VEL_NAVE = 10
