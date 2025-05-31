# Trabajo final 
Materia: Laboratorio de programacion 1


Integrantes: 

Juana Larrumbide 

GitHub: Juana2004

Teresa Moraiz Magadan 

GitHub: teremoraiz


Comision: Lunes


![UML](UML.png)


Este proyecto simula el sistema de gestión que podría utilizar el INCUCAI , encargado de coordinar la donación y el trasplante de órganos y tejidos en Argentina.
La aplicación permite registrar centros de salud, vehiculos, cirujanos, donantes y receptores, gestionar listas de espera, asignar órganos de forma automatizada y simular la logística del transporte y operación médica.
Está pensado como una herramienta que reproduce el proceso detrás de cada trasplante, desde la detección del donante hasta la realización de la cirugía.

# Instalación

Clona el repositorio, crea y activa el entorno virtual y corre el programa:

```bash
git clone https://github.com/Juana2004/SRC.git
cd src
pip install -r requirements.txt
python main.py

# INTERFAZ
El sistema cuenta con una interfaz gráfica desarrollada en Tkinter, que permite una interacción sencilla y directa con las funcionalidades principales del programa, sin necesidad de acceder al código.

Desde la interfaz se puede:

- Ver el estado del incucai
- Registrar donantes (vivos o fallecidos).
- Registrar receptores.
- Consultar la prioridad de un receptor en la lista de espera.
- Ver los receptores registrados en un centro de salud específico.
- Ejecutar el algoritmo de matching, que muestra el resultado del proceso completo: desde la asignación del órgano hasta la operación.
Esta interfaz está diseñada para facilitar la pruebay la visualización del sistema sin necesidad de conocimiento.

#Tener en cuenta:
Por cada ejecucion del codigo se entiende que es un nuevo dia, una vez hecho el match los cirujanos utilizados se marcan como que operaron hoy, si se vuelve a correr el match no estaran disponibles esos cirujanos.

# FUNCIONAMIENTO
-Ingreso de datos iniciales:
    -Receptores con grupo sanguíneo, edad y órganos necesarios.
    -Donantes vivos o fallecidos, con órganos disponibles y compatibilidad sanguínea.
    -Cirujanos (generales y especializados) y su disponibilidad.
    -Centros de salud con ubicación geográfica (provincia, partido y localidad).
    -Vehículos terrestres, helicópteros y aviones, con localización por coordenadas (usando GeoPy).
-Ejecución del algoritmo de matching:
    -Se buscan donantes compatibles con cada receptor según:
        -Grupo sanguíneo.
        -Órgano disponible.
        -Edad compatible.
    -Se verifica que haya cirujanos disponibles en los centros tanto del donante como del receptor.
    -Si los centros son distintos, se evalúa la logística de transporte.
-Transporte de órganos:
    -Se calcula la distancia entre centros mediante coordenadas.
    -Se escoge el vehículo más eficiente según:
        -Distancia.
        -Velocidad.
        -Tráfico (para vehículos terrestres).
        -Disponibilidad (solo se usan vehículos del centro del donante o del receptor).
    -El vehículo seleccionado se desplaza, se actualiza su ubicación y contador de viajes.
-Ablación y operación:
    -Se realiza la ablación (extracción del órgano).
    -Si el donante es vivo, la hora de ablación se asigna en ese momento; si es fallecido, se usa la hora de muerte.
    -Se asegura que el órgano no supere las 20 horas de viabilidad desde la ablación hasta el trasplante contando el tiempo de transporte.
    -Si se supera, el órgano se descarta y el receptor vuelve al tope de la lista de espera.
-Resultado de la operación:
    -Se evalúa la operación con una probabilidad de éxito, influida por si el cirujano es general o especializado.
    -Si la operación es exitosa:
    -Se elimina el receptor del sistema.
    -Se verifica si el donante tiene más órganos para seguir donando.
-Si la operación falla:
    -El órgano se descarta.
    -El receptor vuelve a la lista de espera como prioridad.
    -El donante se conserva si tiene más órganos viables.


