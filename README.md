# Juegos360 - Tienda de Juegos Xbox 360

Una tienda online profesional para la venta de juegos de Xbox 360, desarrollada con Django 4+ e integrada con Mercado Pago para pagos reales.

## 🎮 Características

- **Catálogo completo** de juegos Xbox 360
- **Sistema de carrito de compras** funcional
- **Integración con Mercado Pago** para pagos reales
- **Sistema de pedidos** completo con seguimiento
- **Links de descarga** disponibles después del pago confirmado
- **Panel administrativo** de Django para gestionar juegos
- **Diseño gamer profesional** con tema oscuro moderno
- **Búsqueda y filtros** por género y precio
- **Botón flotante de WhatsApp** para contacto
- **Responsive design** para todos los dispositivos

## 🚀 Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario para el admin**
   ```bash
   python manage.py createsuperuser
   ```

7. **Poblar la base de datos con juegos de ejemplo**
   ```bash
   python manage.py poblar_juegos
   ```

8. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

9. **Abrir en el navegador**
   - Página principal: http://127.0.0.1:8000/
   - Panel admin: http://127.0.0.1:8000/admin/

## 📁 Estructura del Proyecto

```
juegos360/
├── juegos360/          # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── tienda/             # Aplicación principal
│   ├── models.py       # Modelos de datos
│   ├── views.py        # Vistas
│   ├── urls.py         # URLs de la app
│   ├── admin.py        # Configuración del admin
│   ├── templates/      # Plantillas HTML
│   └── management/     # Comandos personalizados
├── static/             # Archivos estáticos (CSS, JS)
│   └── css/
│       └── style.css
├── media/              # Archivos subidos (imágenes)
├── manage.py
└── requirements.txt
```

## 🎯 Funcionalidades

### Para Usuarios

- **Página de inicio** con juegos destacados
- **Catálogo completo** con filtros y búsqueda
- **Páginas de detalle** de cada juego
- **Carrito de compras** con gestión de cantidades
- **Sistema de pedidos** (sin integración de pago real)

### Para Administradores

- **Panel Django Admin** completo
- **Gestión de juegos**: crear, editar, eliminar
- **Gestión de pedidos**: ver y actualizar estados
- **Subida de imágenes** para portadas de juegos

## 🎨 Modelo de Datos

### Juego
- Título
- Descripción
- Género (Acción, RPG, Shooter, etc.)
- Desarrolladora
- Año de lanzamiento
- Clasificación indicativa
- Precio
- Imagen de portada
- Disponible (sí/no)

### Pedido
- Información del cliente
- Total
- Estado (Pendiente, Completado, Cancelado)
- Items del pedido

## 🔧 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Poblar con datos de ejemplo
python manage.py poblar_juegos

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## 📝 Notas

- El proyecto usa SQLite para desarrollo (fácil de cambiar a PostgreSQL/MySQL en producción)
- Las imágenes se guardan en la carpeta `media/juegos/`
- El carrito se gestiona mediante sesiones de Django
- No hay integración de pagos reales (solo simulación de pedidos)

## 🛠️ Tecnologías

- Django 4.2+
- Python 3.8+
- SQLite (desarrollo)
- HTML5 / CSS3
- Pillow (para manejo de imágenes)

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y personal.

---

¡Disfruta explorando la tienda de juegos Xbox 360! 🎮

