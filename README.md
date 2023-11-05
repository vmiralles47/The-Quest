# The Quest
Proyecto final del Bootcamp 0 ed. XVII de Keepcoding. Prototipo del juego "The Quest" con Pygame

Hecho con la versión 2.5.2 de Pygame, y con la 3.10.11 de Python

## Contenido de los archivos y carpetas.

El paquete incluye:
- archivo **main.py**
- carpeta **resources**: incluye los distintos recursos (tipografías, imágenes y sonidos) empleados por el juego.
- carpeta **thequest**. Agrupa los archivos python con el código del juego:
    - ***__init__.py*** : incluye las constantes de configuración del juego. 
    - **game.py**: clase `TheQuest``, cuyo método `jugar()` controla el flujo del juego. 
    - **escenas.py** y **niveles.py** : incluyen las distintas clases correspondientes a las distintas escenas del juego. 
        - Portada
        - Nivel (el juego consta de 4 niveles de creciente dificultad)
        - Gestión de puntuación obtenida
        - Pantalla de records
    - **entidades.py** : incluyen la clases instanciadas por las distintas escenas para poder jugar:
        - `Nave`, `Asteroide`, `Planeta`,`Marcador`, `Contador_Vidas`, `Contador_Niveles` y `Fondo`
    - **records.py** : gestiona la puntuación obtenida y su insercion en la lista persistente de records
    - **dbmanager.py**: incluye los métodos para gestionar la base de datos (records.db) con **Sqlite** y se conecta, escribe y recupera datos del mismo
- carpeta **data** : incluye la base de datos de nombres y puntuaciones, que es el archivo **records.db**.  
    
## Funcionamiento

El juego se arranca con el archivo **main.py**, que invoca a la clase `TheQuest**` ,implementada en el archivo **game.py**

**game.py** instancia una Portada, que incluye bienvenida e instrucciones, y va instanciando niveles según el jugador vaya superando el nivel anterior, hasta un máximo de cuatro. 
Después, muestra siempre si se ha hecho récord o no, y la pantalla de records, desde la cual se puede salir, y volver a jugar.

### Funcionamiento de los niveles
Cada instancia de `Nivel()` recibe como parámetro un número entre 1 y 4 para indicar qué nivel tiene que crear.
A mayor nivel, más y más rápidos asteroides. 

El nivel guarda la puntación y el número de vidas del nivel anterior. 

El nivel genera al ser instanciado un campo de asteorides, que es una lista que va instanciando objetos de la clase `Asteroide`, a los que les asignta un tipo (del 1 al 3), una posición aleatoria y única para cada uno (altura en eje y), y un turno de salida.

Cada ciclo del bucle principal, se actualiza la posición de la nave según las teclas pulsadas, y la posición de los asteroides. 

Si un asteroide colisiona con la nave, se activa el sonido e imagen de explosión, se resta una vida, el asteoride es eliminado de la lista de asteroides ,y todos los asteroides son retrasados la distancia de un ANCHO para dar tiempo a la nave a volver a entrar en juego. 

La nave entra en juego en la posición en que explotó. 

Si se pierden las tres vidas, se acaba la partida y se pasa a la gestión de la puntuación (ver "Haciendo récord" más abajo)

La condición de final de nivel es que la lista de asteroides esté vacía. Es decir, cuando el último asteroide sale por la parte izquierda de la pantalla, es eliminado de la lista y ésta queda vacía. 

Cuando se pasa al estado "final de nivel", controlado por la variable booleana `flag_fin_de_nivel`, la escena toma el control de la nave, moviéndola al centro de la imagen, mientras aparece un planeta por la derecha. Cuando llega al centro, la nave rota 180º sobre su centro y "aterriza" marcha atrás sobre el planeta. El planeta es distinto para cada nivel.

Se guarda la puntuación y el número de vidas restantes y, en cuanto el jugador presione la barra_espaciadora, se instancia el siguiente nivel. 

### Haciendo récord
Al acabar el número de vidas (3) o el último nivel, el juego lanza la escena `pantalla_puntos` si la puntuación obtenida es mayor que las 5 que se guardan en la base de datos **records.db**, el programa pide por pantalla la introducción del nombre del ganador (máximo 10 caracteres). Los muestra mientras se introducen y al pulsar INTRO, se guardan en la base de datos. 

Cada vez, carga la base de datos , la ordena de mayor a menor, inserta el nuevo nombre y puntuación donde corresponda, y reescribe la base de datos entera otra vez, por orden. 

Esta base de datos ya modificada es la que muestra por pantalla la siguiente escena `pantalla_records`



## Desglose de entidades y sus métodos en "entidades.py"

**clase Nave:**
Hereda de la clase `Sprite` de Pygame.
Puede cargar imagen de nave o de explosión (cuando choca con asteroide).
Las imágenes de la nave están en un solo archivo de imagen - **spritesheet_starship.png** - que consta de 3 filas de 16 frames cada una:
- la fila de arriba es para la nave yendo en horizontal
- la fila central es para la nave bajando
- la fila de abajo es para la nave subiendo

El método `update` recorre con un frame el archivo de imágenens e "imprimiendo" la que corresponde en cada momento en la surface que muestra el juego. 
Y lo mismo para las explosiones con el método  `update_explosion`.
Cuando se llega al final de nivel, `update_rotacion` y  `update_va_al_centro` se encargan de controlar la nave,rotarla y hacerla aterrizar en el planeta. 

Además carga un sonido para la explosión y otro para la navegación entre asteroides, que se activan y desactivan desde la escena `Nivel()` cuando corresponde.

La velocidad de la nave es **inercial**: cuanto más tiempo se aprieta el botón(sea la flecha UP o la flecha DOWN) sin soltarlo, más rápido va, hasta un limíte de 10 veces su velocidad inicial. al soltar el botón, la velocidad se resetea.

**class Asteroide:**
Hereda de la clase `Sprite`` de Pygame.
Al ser instanciados reciben como parámetro: 
- Altura: una posición única en y desde la que saldrán.
- Tipo (de 1 a 3): determina su velocidad, tamaño y puntuación que genera al salir de la pantalla por el margen izquierdo.
- Turno: una cantidad que con un cotandor irá dismiuyendo y cuando llega a cero, lanza al asteroide.

Al contrario que la nave (que carga una tira de imágenes de la que luego va cogiendo la que le interesa), los asteorides cargan, según su tipo, 16 imágenes cada uno en una lista de imágenes, para generar la ilusión de rotación.

Cada tipo de asteroide tiene una velocidad constante. Los pequeños son más rápidos y los grandes más lentos.

Sú único método es `update`, que actualiza la posición según la velocidad.
El resto de la gestión de Asteroides la hace la escena `Nivel` como se ha descrito anteriormente.


**clases Marcador, Contador_vidas, Contador_niveles**
Cada una se encarga de la cifra correspondiente: Puntuación obtenida, vidas y nivel.
Al ser instanciados cogen el valor por defecto: 0 puntos, 3 vidas, nivel 1, y luego tienen métodos muy básicos para modificar  ese valor, ser consultados por la escena Nivel cuando sea necesario, y resetearse.


**clase Fondo**
Gestiona el bucle sin fin del fondo de cada escena `Nivel`. 

**clase Planeta**
Se instancia recibiendo el número de nivel como parámetro, eso permite comportamientos distintos según el nivel recibido.

Para cada nivel, carga una imagen de planeta distinto según el nivel. Aunque el comportamiento de todos ellos es el mismo: empiezan a salir cuando se da la condicion de fin de nivel, y se mueven a velocidad constante hasta que su centro queda alineado con el margen derecho de la pantalla.

Como no todos tienen exactamente el mismo tamaño, le pasan su coordenada `rect.left` al método de la nave `update_rotacion`, para que éste pueda calcular el lugar de aterrizaje de la nave, que es la mitad de la distancia entre el limíte izquierdo del planeta y el ancho de la pantalla.








