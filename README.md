# libRoom
A writing software.
More than a rich text processor, libRoom seeks to meet the needs of writing and managing narrative projects by using a local database customized for each user. Therefore, it is aimed at writers and poets.

# Commands to work with the backend
Abrir el cmd (no puede ser el PowerShell), ejecutar los siguientes comandos: 

cd libRoom (para abrir el proyecto global, que incluye tanto el frontend como el backend).

cd libRoom_backend

venv\Scripts\activate.bat <!-- activa el entorno virtual, indicado de esta forma en el cmd: (venv) C:/users/tu_usuario/proyecto -->

pip install django djangorestframework <!--solo la primera vez que se abra el proyecto -->

pip install -r requirements.txt <!--en este documento se listan todas las liberías que se utilizarán en este proyecto, en el mismo se deben incluir las librerías que se vayan instalando en el futuro -->

pip freeze > <!--requirements.txt para actualizarlo cada vez que se instala una nueva librería -->

deactivate  <!--para cerrar el entorno virtual luego de terminar de trabajar. -->

<!-- traducir antes de entregar el repositorio -->