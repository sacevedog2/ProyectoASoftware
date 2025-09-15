# ProyectoASoftware

Este proyecto es una aplicación web de una tienda online de ropa desarrollada con Django.

## Requisitos previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

## Instalación de dependencias

Ejecuta el siguiente comando en la raíz del proyecto para instalar todas las dependencias necesarias:

```powershell
pip install -r requirements.txt
```

## Ejecución del servidor de desarrollo

Para iniciar el servidor de desarrollo de Django, ejecuta el siguiente comando en la raíz del proyecto:

```powershell
python manage.py runserver
```

## Acceso a la aplicación

Una vez iniciado el servidor, abre tu navegador y accede a la siguiente URL principal:

```
http://127.0.0.1:8000/
```

Esta es la ruta principal de la aplicación.

## Notas adicionales
- Asegúrate de tener configurada la base de datos correctamente antes de ejecutar el servidor.
- Si necesitas aplicar migraciones, ejecuta:

```powershell
python manage.py migrate
```

- Para crear un superusuario (opcional):

```powershell
python manage.py createsuperuser
```
