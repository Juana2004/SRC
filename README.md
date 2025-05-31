# **Trabajo final**
### Materia: Laboratorio de programacion 1
### Integrantes: 
    Juana Larrumbide 
    GitHub: Juana2004

    Teresa Moraiz Magadan 
    GitHub: teremoraiz
### Comision: Lunes


![UML](UML.png)

Este proyecto simula el sistema de gestión que podría utilizar el INCUCAI , encargado de coordinar la donación y el trasplante de órganos y tejidos en Argentina.
El sistema permite registrar centros de salud, vehiculos, cirujanos, donantes y receptores, gestionar listas de espera, asignar órganos de forma automatizada y simular la logística del transporte y operación médica.
Está pensado como una herramienta que reproduce el proceso detrás de cada trasplante, desde la detección del donante hasta la realización de la cirugía.

## Instalación

Abrir carpeta de preferencia en Visual Studio Code y ejecutar en terminal:
```bash
git clone https://github.com/Juana2004/SRC.git
cd src
python -m venv venv

Windows:
venv\Scripts\activate

MacOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
### Formato utilizado
Para este proyecto se utilizo la extension Black Formatter, utilizada comunmente en proyectos en python + Estilos de codigo vistos en clase.

## Interfaz
El sistema cuenta con una interfaz gráfica desarrollada en Tkinter, que permite una interacción sencilla y directa con las funcionalidades principales del programa, sin necesidad de acceder al código.

### Desde la interfaz se puede:

- Ver el estado del incucai: Cantidad de vehiculos, cirujanos, donantes, receptores y centros de salud. La lista de donantes y receptores.
- Registrar donantes (vivos o fallecidos).
- Registrar receptores.
- Consultar la prioridad de un receptor en la lista de espera.
- Ver los receptores registrados en un centro de salud específico.
- Ejecutar el algoritmo de matching, que muestra el resultado del proceso completo: desde la asignación del órgano hasta la operación.
Esta interfaz está diseñada para facilitar la prueba y la visualización del sistema sin necesidad de conocimiento.

### Tener en cuenta:
Por cada ejecucion del codigo se entiende que es un nuevo dia, una vez hecho el match los cirujanos utilizados se marcan como que operaron hoy, si se vuelve a correr el match no estaran disponibles esos cirujanos. Los vehiculos utilizados tendran su ubicacion actualizada, no tendran la que fue inicializada y su contador de viajes sera mayor a 0. Por su parte, los receptores y donantes podran o no estar, dependiendo de si tuvieron una operacion exitosa o no, y para el caso de los donantes, los fallecidos; la hora de ablacion de sus organos ya estaria asignada con su hora de fallecimiento, para los vivos; La hora de ablacion del organo se asigna una vez hecha la ablacion, por lo tanto, aunque haya donado un organo antes los demas no tendran asignada una hora aun.

### Implementacion de libreria GeoPy
Para la gestión de transporte dentro del sistema de trasplantes, se utilizó la librería GeoPy de Python, la cual permite realizar operaciones geográficas a partir de coordenadas (latitud y longitud).

-Funcionalidades implementadas con GeoPy:
    -Asignación inicial de ubicaciones:
        A cada centro de salud y vehículo se le asigna una ubicación geográfica del tipo {Direccion, Partido, Provincia, Pais}, para uso eficiente se recomienda escribir direcciones reales y contar con una velocidad minima de internet de 1–5 Mbps ya que se convierten direcciones a coordenadas: geocodificación, para esto se consulta al servicio Nominatin. 
        Cálculo de distancias
    -Se utiliza GeoPy para calcular la distancia en kilómetros entre:
        - **Tener en cuenta:** El calculo realizado es entre dos coordenadas, GeoPy **no** simula la ruta real como si fuera un gps.
        -Dos centros de salud.
        -Un centro y un vehículo.
        -La ruta de un vehículo en movimiento (para estimar tiempos de llegada).
    -Actualización de ubicación
        Cada vez que un vehículo inicia un viaje para transportar un órgano, su posición se actualiza al llegar al destino. Este comportamiento se simula mediante el cálculo de distancias y la actualización de coordenadas. 

### Nota sobre GeoPy
A pesar de tener una conexion baja, internamente GeoPy realiza los calculos a partir de coordenadas por lo que las ubicaciones si se actualizan, solo que la geocodificacion no funcionaria por eso no se podria imprimir la nueva direccion. A pesar de eso, para mayor orden de codigo si al momento de registrar un Objeto de tipo Vehiculo o CentroDeSalud no se logra geocodificar, este no se registrara, y por consecuencia, como todas las demas clases son composicion de CentroDeSalud tampoco se registraran. En cambio, al momento de actualizar la ubicacion de un vehiculo, si no se logra geocodificar, el programa seguira funcionando igual pero no se podra ver la nueva ubicacion de este, pero internamente GeoPy hara bien los calculos de distancias.

## FUNCIONAMIENTO
-Ingreso de datos iniciales:
    -Receptores con grupo sanguíneo, edad y órgano necesario: Estos entran en una lista de espera ordenados por prioridad.
        -Prioridad:
            -Estado: estable/inestables. Al iniciar todos son estables, pasan a ser inestables si su operacion falla.
            -Patologia: hay preescritas en tipos/patologias.py aproximadamente 3/4 patologias dependiendo del organo que se requiere, cada una puede tener prioridad media o baja, en caso de tener otra, se puede seleccionar "otra" y se contempla como prioridad baja.
            -Urgencia: Se entiende como un choque o accidente de ese tipo.
            -Fecha en que entro a la lista: Si todo lo anterior da la misma prioridad para dos receptores, estara primero el que entro antes a la lista.
    -Donantes vivos o fallecidos, con órganos disponibles.
    -Cirujanos (generales y especializados).
    -Centros de salud con ubicación geográfica (provincia, partido y localidad).
    -Vehículos terrestres, helicópteros y aviones, con ubicación geográfica (provincia, partido y localidad).
-Ejecución del algoritmo de matching:
    -Se buscan donantes compatibles con cada receptor según:
        -Grupo sanguíneo.
        -Órgano disponible.
        -Edad compatible.
        **nota** Los criterios utilizados fueron los mas parecidos a la realidad, se pueden ver en el archivo sistema/compatibilidad.py
    -Se verifica que haya cirujanos disponibles en los centros tanto del donante como del receptor: Uno realizara la ablacion y otro el trasplante de organo.
    -Si los centros son distintos, se evalúa la logística de transporte: Se asegura que haya un vehiculo del tipo necesitado que pertenzca al centro del donante o del receptor.
-Ablación:
    -Se realiza la ablación (extracción del órgano).
    -Si el donante es vivo, la hora de ablación se asigna en ese momento; si es fallecido, se usa la hora de muerte.
-Transporte de órganos:
    -Se calcula la distancia entre centros mediante coordenadas.
    -Se escoge el vehículo más eficiente según:
        -Distancia.
        -Velocidad.
        -Tráfico (para vehículos terrestres).
        -Disponibilidad (solo se usan vehículos del centro del donante o del receptor).
        **nota:** El calculo realizado es distancia/velocidad = tiempo , en caso de ser terrestre el trafico es calculado con un random. 
    -El vehículo seleccionado se desplaza, se actualiza su ubicación y contador de viajes.
-Resultado de la operación:
    -Se asegura que el órgano no supere las 20 horas de viabilidad desde la ablación hasta el trasplante contando el tiempo de transporte.
    -Si se supera, el órgano se descarta y el receptor vuelve a la posicion 1 de la lista de espera.
    -Se evalúa la operación con una probabilidad de éxito, influida por si el cirujano es general o especializado.
        -Si la operación es exitosa:
            -Se elimina el receptor del sistema.
            -Se verifica si el donante tiene más órganos para seguir donando, en caso contrario, se elimina.
        -Si la operación falla:
            -El órgano se descarta.
            -El receptor vuelve a la lista de espera a la posicion 1.
            -El donante se conserva si tiene más órganos viables.

## Metodos Magicos utilizados
- __eq__ : utilizado en las clases Cirujano: compara si dos cirujanos tienen misma cedula, Centro de salud: compara si dos centros tienen mismo nombre y direccion, y Paciente: compara si dos pacientes tienen mismo dni.

- __hash__ : utlizado en Centro de salud: devuelve un número entero que representa de manera única a un objeto, Python primero compara los hashes para ver si puede evitar usar __eq__ que es menos eficiente.

- __lt__ : Compara dos receptores para definir cual tiene mayor prioridad, luego se usa sort() sobre la lista de estos y los ordena automaticamente.

- __str__ : Utilizado en incucai, muestra el estado del incucai solo printeado al objeto.

-Utilizado en salida_metodos:

    - __enter__ :  Para preparar el recurso que se va a usar en el bloque with, redirige la salida estándar (print) al buffer interno.

    - __exit__ : Se ejecuta al salir del bloque 'with' para restaurar la salida estándar al valor original.
