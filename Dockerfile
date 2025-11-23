# Imagen base oficial de Python
FROM python:3.11-slim

# Variables de entorno recomendadas para Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos de requerimientos e instalarlos
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Puerto en el que se expondrá la aplicación
EXPOSE 8000

# Comando por defecto: migrar y levantar servidor con gunicorn
CMD ["bash", "-c", "python manage.py migrate && gunicorn ProyectoASoftware.wsgi:application --bind 0.0.0.0:8000"]
