# Editor view
Reutiliza el widget de edición de texto, que tiene un contador de palabras y muestra arriba el título (campo *title*) de lo que se esté editando

a la derecha un selector de capítulos, que habilita el selector de escena (para escoger qué archivo editar, guarse por el campo ID de la escena, ). 

En la sección de metadatos de escena se pueden editar el objetivo en palabras de la escena (campo "*setGoal*"del scene_x.md), cuyo dato se muestra en la parte superior, comparando con la cantidad de palabras que se han escrito (ej. 250/1700 palabras). También cambiar el estatus (tomar las opciones del tags.txt). Selector de POV (despliega los personajes creados, asignando su nombre al campo POV del scene_x.md)

Un buscador de notas (muestra las notas existentes asociadas al capítulo, buscándo en el notes_index.json de la carpeta notes/, buscando el notes_path dentro del project.json), sino, mostrar un creador de nota pequeño, que asocia directamente la nota a la escena, editando el título y dos líneas (guardar la nota en el notes.json)