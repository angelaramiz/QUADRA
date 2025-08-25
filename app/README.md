# 🚀 QUADRA - Aplicación Principal

**Directorio de la aplicación Flask**

## 📁 Estructura de la aplicación

```
app/
├── models/              # 🗃️ Modelos de base de datos
│   ├── __init__.py     #   📦 Inicialización de modelos
│   ├── user.py         #   👤 Modelo de usuario
│   ├── food_stand.py   #   🍔 Modelo de puesto de comida
│   └── review.py       #   ⭐ Modelo de reseñas
├── routes/              # 🚏 Rutas y controladores
│   ├── __init__.py     #   📦 Inicialización de blueprints
│   ├── main.py         #   🏠 Rutas principales
│   ├── auth.py         #   🔐 Autenticación
│   └── food_stands.py  #   🍕 CRUD de puestos
├── templates/           # 📄 Plantillas HTML Jinja2
│   ├── base.html       #   🏗️ Plantilla base
│   ├── landing.html    #   🌟 Página de inicio
│   ├── dashboard.html  #   📊 Dashboard principal
│   ├── auth/           #   🔐 Templates de autenticación
│   └── food_stands/    #   🍔 Templates de puestos
├── static/              # 🎨 Archivos estáticos
│   ├── css/            #   🎨 Hojas de estilo
│   ├── js/             #   ⚡ JavaScript
│   └── uploads/        #   📸 Imágenes subidas
├── migrations/          # 🔄 Migraciones de base de datos
├── instance/            # 💾 Base de datos SQLite (desarrollo)
├── .env                 # ⚙️ Variables de entorno (no commitear)
├── .env.example         # 📋 Ejemplo de configuración
├── __init__.py          # 📦 Factory de la aplicación
├── run.py               # 🎬 Punto de entrada
└── setup_postgres.py    # 🐘 Configurador PostgreSQL
```

## 🚀 Ejecutar la aplicación

### Desde esta carpeta (`app/`):
```bash
python run.py
```

## 🔧 Comandos de desarrollo

### Migraciones de base de datos:
```bash
# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Ver historial
flask db history

# Downgrade (rollback)
flask db downgrade
```

### Variables de entorno:
```bash
# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones
```

### PostgreSQL:
```bash
# Configurar PostgreSQL
python setup_postgres.py
```

## 📊 Modelos de datos

### 👤 User (Usuario)
- `id` - Identificador único
- `username` - Nombre de usuario (único)
- `email` - Email (único)
- `password_hash` - Hash seguro de contraseña
- `created_at` - Fecha de registro

### 🍔 FoodStand (Puesto de Comida)
- `id` - Identificador único
- `name` - Nombre del puesto
- `description` - Descripción
- `latitude/longitude` - Coordenadas GPS
- `address` - Dirección textual
- `food_type` - Tipo de comida
- `image_filename` - Archivo de imagen
- `user_id` - Usuario propietario

### ⭐ Review (Reseña)
- `id` - Identificador único
- `rating` - Calificación (1-5 estrellas)
- `comment` - Comentario
- `user_id` - Usuario que reseña
- `food_stand_id` - Puesto reseñado

## 🎯 Blueprints y rutas

### Main (`routes/main.py`)
- `/` - Página principal
- `/dashboard` - Dashboard del usuario

### Auth (`routes/auth.py`)
- `/auth/login` - Inicio de sesión
- `/auth/register` - Registro
- `/auth/logout` - Cerrar sesión

### Food Stands (`routes/food_stands.py`)
- `/food-stands/` - Lista de puestos
- `/food-stands/create` - Crear puesto
- `/food-stands/<id>` - Ver puesto
- `/food-stands/<id>/edit` - Editar puesto
- `/food-stands/my-stands` - Mis puestos

## 🔒 Configuración de seguridad

La aplicación incluye:
- ✅ **Protección CSRF** con Flask-WTF
- ✅ **Hash de contraseñas** con Werkzeug
- ✅ **Rate limiting** con Flask-Limiter
- ✅ **Validación de formularios** robusta
- ✅ **Sesiones seguras** con Flask-Login

## 🗃️ Base de datos

### SQLite (Desarrollo)
Archivo: `instance/quadra.db`

### PostgreSQL (Producción)
Configuración en `.env`:
```
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/quadra_db
```

---

**🔧 Para desarrollo, ejecuta:** `python run.py`  
**📚 Para documentación completa, ve al:** [`README.md`](../README.md) principal
