# Project manager menu
    
título de la pantalla: Create a new project, centrado a la mitad de la ventana y a una distancia de 50 píxeles de la parte superior de la ventana.
lo que sigue debe estar en un contenedor a 108 píxeles de la parte superior, y  173 de la parte izquierda, centrado, contiene lo siguiente:

## template options

(esto aparece como una columna, el títullo es pick a template, debajo hay dos botones, preferiblemente un input-event que no se vea como un botón, si no como una cinta con el texto al darle clic aparece el editor de estadísticas)
Pick template
- Prose
    - Tale (type = "short_story")
    - Novel (type = "novel")

## buttons

estos botones deben estar debajo del editor de estadísticas, hacia la parte derecha.
open file (abre el sistema de archivos del usuario, la primera vez en directorio raíz, las siguientes en la última ubicación dónde se guardó). en este caso se obtienen los datos del proyecto.

create: crea un nuevo proyecto, llamando a la lógica de creación de proyecto en la api, guardando la carpeta en un directorio escogido por el usuario y enviándole la información

al abrir un proyecto, leer el settings.json y el preferences.json y cargar las configuraciones que se encuentren en estos, hacer configuraciones por defecto. 
## statistics editor

No. of chapters (solo en la opción novela): campo de texto para escribir la cantidad de capítulos, y un spinbox con el que mover los números.

No. of scenes: el mismo contenido que en el anterior (opción tanto en novela como en cuento).

words per scene:  campo de texto y spinbox

Total words: total de palabras del proyecto, que se actualice a medida que se cambien los campos anteriores, además no manda datos a la API, solo los tres campos anteriores.


# General view
Campos de texto:
Title:
Author: 
<!-- añadir estos campos al project_initializer.py -->
Series: 
Volume: 
Genres:
License:
Author e-mail: 

Botón create: guarda los datos en el project.json <!-- añadir lógica de guardado al project-app, aunque probablemente no sea necesario, otra forma es que al editar desde acá, al darle a guardar se cambia el archivo, archivo que leerá de nuevo project-app cuando el proyecto se vuelva a abrir.--->