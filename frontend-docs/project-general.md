# Project manager menu

## template options
Pick template
- Prose
    - Tale (type = "short_story")
    - Novel (type = "novel")

## buttons
open file (abre el sistema de archivos del usuario, la primera vez en directorio raíz, las siguientes en la última ubicación dónde se guardó alo).

create: crea un nuevo proyecto, llamando a la lógica de creación de proyecto en la api, guardando la carpeta en un directorio escogido por el usuario.

## statistics editor

No. of chapters (solo en la opción novela): campo de texto para escribir la cantidad de capítulos, y un spinbox con el que mover los números.

No. of scenes: el mismo contenid que en el anterior (opción tanto en novela como en cuento).

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

Botón save: guarda los datos en el project.json <!-- añadir lógica de guardado al project-app, aunque probablemente no sea necesario, otra forma es que al editar desde acá, al darle a guardar se cambia el archivo, archivo que leerá de nuevo project-app cuando el proyecto se vuelva a abrir.--->