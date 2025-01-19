# Tasks App

Tasks App es una aplicación de escritorio para la gestión de tareas, construida utilizando Python, SQLite, Tkinter y SQLAlchemy.

## Descripción de Archivos

- `main.py`: Archivo principal que inicia la aplicación.
- `models/database.py`: Define la clase `DataBase` para interactuar con la base de datos SQLite.
- `models/task.py`: Define la clase `Task` que representa una tarea en la base de datos.
- `viewmodels/tasks_viewmodel.py`: Define la clase `TasksViewModel` que maneja la lógica de negocio de la aplicación.
- `views/tasks_view.py`: Define la clase `TasksView` que maneja la interfaz gráfica de usuario utilizando Tkinter.
- `requirements.txt`: Lista de dependencias del proyecto.


## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv env
    source env/Scripts/activate  # En Windows
    source env/bin/activate      # En Unix o MacOS
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Ejecuta la aplicación:
    ```sh
    python main.py
    ```

2. La interfaz gráfica se abrirá y podrás agregar, editar, eliminar y marcar tareas como completadas.
