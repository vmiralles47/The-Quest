# The-Quest
Proyecto final del Bootcamp 0 ed. XVII de Keepcoding. Prototipo del juego "The Quest" con Pygame

Hecho con la versión 2.5.2 de Pygame, y con la 3.10.11 de Python

##Contenido de los archivos y carpetas
El paquete incluye:
- archivo **main.py**
- carpeta **resources**: incluye los distintos recursos (tipografías, imágenes y sonidos) empleados por el juego.
- carpeta **thequest**. Agrupa los archivos python con el código del juego:
    - __init__.py : incluye las constantes de configuración del juego. 
    - **game.py**: clase TheQuest, cuyo método `jugar()` controla el flujo del juego. 
    - **escenas.py** y **niveles.py** : incluyen las distintas clases correspondientes a las distintas escenas del juego. 
        - Portada
        - Nivel (el juego consta de 4 niveles de creciente dificultad)
        - Gestión de puntuación obtenida
        - Pantalla de records
    - **entidades.py** : incluyen la clases instanciadas por las distintas escenas para poder jugar:
        - Nave, Asteroide, Planeta, Marcador, Contador_vidas, Contador_niveles y Fondo
    - **records.py** : gestiona la puntuación obtenida y su insercion en la lista persistente de records
    - **dbmanager.py**: incluye los métodos para gestionar la base de datos (records.db) con **Sqlite** y se conecta, escribe y recupera datos del mismo
- carpeta **data** : incluye la base de datos, que es el archivo records.db.  
    
## Funcionamiento

El juego se arranca con el archivo **main.py**, que invoca a la clase **TheQuest** ,implementada en el archivo **game.py**

**game.py** instancia una Portada, que incluye bienvenida e instrucciones, y va instanciando niveles según el jugador vaya superando el nivel anterior, hasta un máximo de cuatro. 
Después, muestra siempre si se ha hecho récord o no, y la pantalla de records, desde la cual se puede salir, y volver a jugar.

### Funcionamiento de los niveles
Cada instancia de Nivel() recibe como parámetro un número entre 1 y 4 para indicar qué nivel tiene que crear.
A mayor nivel, más asteroides, y con más velocidad. 

El nivel guarda la puntación y el número de vidas del nivel anterior. 

El nivel genera al ser instanciado un campo de asteorides, que es una lista que va instanciando objetos de la clase Asteroide, a los que les asignta un tipo (del 1 al 3), una posición aleatoria  y única para cada uno (altura en eje y), y un turno de salida.

La condición de final de nivel es que la lista esté vacía. Es decir ,cuando el último asteroide sale por la parte izquierda de la pantalla, es eliminado de la lista y ésta queda vacía. 

Cuando se pasa al estado "final de nivel", controlado por la variable booleana `flag_fin_de_nivel`, la escena toma el control de la nave, moviéndola al centro de la imagen, mientras aparece un planeta por la derecha. cuando llega al centro, la nave rota 180º sobre su centro y "aterriza" marcha atrás sobre el planeta.

Se guarda la puntuación y el número de vidas restantes y, en cuanto el jugador presione la barra_espaciadora, se instancia el siguiente nivel. 

### Haciendo récord
Al acabar el número de vidas (3) o el último nivel, el juego lanza la escena `pantalla_puntos` si la puntuación obtenida es mayor que las 5 que se guardan en la base de datos **records.db**, el programa pide por pantalla la introducción del nombre del ganador (máximo 10 caracteres). Los muestra mientras se introducen y al pulsar INTRO, se guardan en la base de datos. 

Cada vez, carga la base de datos , la ordena de mayor a menor, inserta el nuevo nombre y puntuación donde corresponda, y reescribe la base de datos entera otra vez, por orden. 

Esta base de datos ya modificada es la que muestra por pantalla la siguiente escena `pantalla_records`



## Desglose de entidades y sus métodos en "entidades.py"




**clase Nave:**
Hereda de la clase Sprite de Pygame
Puede cargar imagen de nave o de explosión (cuando choca con asteroide)
las imágenes de nave están en un solo archivo de imagen que consta de 3 filas de 16 frames cada una:
- la fila de arriba es para la nave yendo en horizontal
- la fila central es para la nave bajando
- la fila de abajo es para la nave subiendo

El método `update` recorre con un fotograma el archivo de imágenens e "imprimiendo" en la surface que muestra el juego la que corresponde en cada momento. 
V lo mismo para las explosiones con el método  `update_explosion` 
Cuando se llega al final de nivel, `update_rotacion` y  `update_va_al_centro` se encargan de controlar la nave ,rotarla y hacerla aterrizar en el planeta. 

Además carga un sonido para la explosión y otro para la navegación entre asteroides, que se activan y desactivan desde la escena Nivel() cuando corresponde.

La velocidad de la nave es inercial: cuanto más tiempo se aprieta el botón(sea la flecha UP o la flecha DOWN) sin soltarlo, más rápido va, hasta un limíte de 10 veces su velocidad inicial. al soltar el botón, la velocidad se resetea.

**class Asteroide:**
Hereda de la clase Sprite de Pygame.
Al ser instanciados reciben como parámetro: 
- Altura: una posición única en y desde la que saldrán
- Tipo (de 1 a 3): determina su velocidad, tamaño y cuantos puntos genera al salir por la izquierda
- Turno: una cantidad qeu con un cotandor irá dismiuyendo y cuando llega a cero, lanza al asteroide

Al contrario que la nave (que carga una tira de imágenes de la que luego va cogiendo la que le interesa), los asteorides cargan, según su tipo, 16 imágenes cada uno en una lista de imágenes, para generar la ilusión de rotación.

Y aunque la velocidad básica depende del tipo que sean, esa velocidad es constante.

Sú único método es `update`, que actualiza la velocidad
El resto de la gestión de Asteroides la hace la escena `Nivel` como se ha descrito anteriormente.



**clases Marcador, Contador_vidas, Contador_niveles**
Cada una se encarga de la cifra correspondiente: Puntuación obtenida, vidas y en qué nivel
Al ser instanciados cogen el valor por defecto: 0 puntos, 3 vidas, nivel 1, y luego tienen métodos muy básicos para modificar  ese valorm¡,  ser consultados por la escena Nivel cuando sea necesario ,y resetearse.

**clase Fondo**


2. pintar (aparece por la izquierda en el FINAL DE NIVEL para que la nave aterrice en él)

**clase Planeta**
1. crear según nivel (asignar imagen)
2. pintar (se desplaza hacia la izquierda para generar sensación de movimiento. puede ser una imagen sinfin que se repita, o sea dos imagenes que vaya alternando)


## Métodos del juego
- posiciona el jugador DONE
- pinta el jugador según se mueva DONE
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


