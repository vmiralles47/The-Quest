# Desglose de entidades y métodos

## Entidades

**jugador**
Es la nave mueve en vertical en el margen derecho
Será un sprite para poder generar la explosión cuando choque con un asteroide
métodos:
1. Crear: carga las imágenes/define el polígono y poco más
2. pintar
3. mover (arriba y abajo hasta los limites de la pantalla)
4. explotar
5. aterrizar 

**asteroide**
Podrán tener una velocidad y un tamaño
cargarán una imagen u otra en función de qué tipo sean
métodos:
1. Crear(tamaño, velocidad) (o tipo)
2. Pintar
3. Moverse (velocidad o tipo)
4. Avisa si sale de la pantalla por el margen izquierdo

**campo de asteroides**
segun el nivel, genera x asteroides con distintas velocidades y tamaños
1. crear: 
2. pintar - pinta todos sus asteroides
3. asignar tamaño
4. asignar velocidad
5. asignar posicion inicial 
6. resetear¿?

**marcador**
métodos
1. crear (por defecto a 0 puntos)
2. pintar
3. incrementar(incremento)
4. resetear

**contador de vidas**
métodos
1. crear (por defecto a NUM_VIDAS del __init__)
2. pintar
3. restar vida
4. resetear

**fondo**
1. crear según nivel (asignar imagen)
2. pintar (aparece por la izquierda en el FINAL DE NIVEL para que la nave aterrice en él)

**planeta**
1. crear según nivel (asignar imagen)
2. pintar (se desplaza hacia la izquierda para generar sensación de movimiento. puede ser una imagen sinfin que se repita, o sea dos imagenes que vaya alternando)


## Métodos del juego
- posiciona el jugador 
- pone el fondo en movimiento
- según el nivel, crea el campo de asteroides
- Lanza los asteorides hasta que se acaben los de ese nivel
- Si los asteorides van saliendo por la izquierda, incrementa el contador
- si un asteoride choca con la nave, resta una vida. Si se acaban las vidas , se acaba el juego. 
- si se cumple la **condicion fin de nivel**, se lanza el método "acabar_nivel" y pasa al siguiente. Si era el último, 
se acaba el juego 
- al final, muestra la pantalla de records

### método "acabar_nivel"
- aparece el planeta por la derecha
- la nave avanza, rota sobre si misma y se mueve hasta *aterrizar* en el planeta. los asteroides restantes no le afectan.
- si es el ultimo nivel, se comprueba si hay recórd. Si lo hay, se piden iniciales en pantalla 
- si no es el último nivel sale mensaje de enhorabuena y al pulsar barra se pasa al nivel dos. se mantienen vidas y puntuación

