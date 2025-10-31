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

## 🔄 Compilar Traducciones

Si modificas las traducciones en `locale/en/LC_MESSAGES/django.po`, debes recompilar:

```powershell
python compile_translations.py
```

**Nota**: Los precios en la base de datos están en **Peso Colombiano (COP)** como moneda base.


## API REST - Documentación de Productos (Solo Lectura)
API REST de solo lectura en formato JSON para consultar los productos del catálogo de Silhouette.

**Nota:** Esta API solo permite operaciones de lectura (GET). No se pueden crear, modificar o eliminar productos a través de esta API.

### 🔗 Base URL
```
http://localhost:8000/api/
```

**Nota:** La API no requiere prefijo de idioma (`/es/` o `/en/`), funciona directamente desde `/api/`

---

### 📋 Endpoints Disponibles

### 1. Listar todos los productos
**GET** `/api/productos/`

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "productos": [
    {
      "id": 1,
      "nombre": "Camiseta Básica",
      "descripcion": "Camiseta de algodón 100%",
      "precio": 29990,
      "stock": 50,
      "talla": "S,M,L,XL",
      "tallas_disponibles": ["S", "M", "L", "XL"],
      "color": "Negro",
      "tipo": "camiseta",
      "genero": "hombre",
      "imagen": "/media/productos/camiseta1.jpg"
    },
    {
      "id": 2,
      "nombre": "Buzo Deportivo",...}}
      
```

### 2. Obtener detalle de un producto
**GET** `/api/productos/{id}/`

**Parámetros:**
- `id` (int): ID del producto

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "producto": {
    "id": 1,
    "nombre": "Camiseta Básica",
    "descripcion": "Camiseta de algodón 100%",
    "precio": 29990,
    "stock": 50,
    "talla": "S,M,L,XL",
    "tallas_disponibles": ["S", "M", "L", "XL"],
    "color": "Negro",
    "tipo": "camiseta",
    "tipo_display": "Camiseta",
    "genero": "hombre",
    "genero_display": "Hombre",
    "imagen": "/media/productos/camiseta1.jpg"
  }
}
```

**Respuesta de error (404 Not Found):**
```json
{
  "success": false,
  "error": "Producto no encontrado"
}
```
---

### 3. Buscar productos
**GET** `/api/productos/buscar/`

**Parámetros de query (opcionales):**
- `q` (string): Texto de búsqueda en el nombre
- `tipo` (string): Tipo de prenda (`camiseta`, `buzo`, `pantalon`)
- `genero` (string): Género (`hombre`, `mujer`)
- `precio_min` (float): Precio mínimo
- `precio_max` (float): Precio máximo

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "filtros": {
    "q": "camiseta",
    "tipo": "camiseta",
    "genero": "hombre",
    "precio_min": "20000",
    "precio_max": "50000"
  },
  "productos": [
    {
      "id": 1,
      "nombre": "Camiseta Básica",
      "descripcion": "Camiseta de algodón 100%",
      "precio": 29990,
      "stock": 50,
      "talla": "S,M,L,XL",
      "color": "Negro",
      "tipo": "camiseta",
      "genero": "hombre",
      "imagen": "/media/productos/camiseta1.jpg"
    }
  ]
}
```

## 🔐 Seguridad

**Solo lectura:**

### 🧪 Pruebas 

1. **GET** Lista de productos: `http://localhost:8000/api/productos/`
2. **GET** Detalle producto: `http://localhost:8000/api/productos/1/`
3. **GET** Buscar: `http://localhost:8000/api/productos/buscar/?q=camiseta`

---

### 📝 Códigos de estado HTTP

- `200 OK`: Solicitud exitosa
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor
