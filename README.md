# 🌮 Quadra - Plataforma de Puestos de Comida

<div align="center">

![Quadra Logo](https://img.shields.io/badge/Quadra-Food%20Stands-orange?style=for-the-badge&logo=restaurant)

**Descubre, comparte y califica los mejores puestos de comida callejera de tu ciudad**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue?style=flat-square&logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[🚀 Demo](#demo) • [📖 Instalación](#instalación) • [🎯 Características](#características) • [🤝 Contribuir](#contribuir)

</div>

---

## 📋 Descripción

**Quadra** es una aplicación web desarrollada con Flask que permite a los usuarios descubrir, agregar y calificar puestos de comida callejera. Los usuarios pueden compartir ubicaciones georeferenciadas, subir fotos, escribir reseñas y encontrar los mejores sabores de su ciudad.

### 🎯 Características Principales

- 🗺️ **Mapas Interactivos** - Ubicación precisa con Leaflet
- ⭐ **Sistema de Reseñas** - Calificaciones de 1-5 estrellas
- 📸 **Subida de Imágenes** - Fotos de alta calidad con optimización automática
- 🔐 **Autenticación Segura** - Registro y login con validaciones robustas
- 📱 **Diseño Responsive** - Compatible con móviles y tablets
- 🔍 **Búsqueda y Filtros** - Encuentra exactamente lo que buscas

## 🚀 Demo

### Pantallas Principales

| Página Principal | Lista de Puestos | Detalle del Puesto |
|:----------------:|:----------------:|:------------------:|
| Mapa interactivo con todos los puestos | Lista paginada con filtros | Vista detallada con reseñas |

> **Nota:** Las imágenes de demo se encuentran en la carpeta [`img/`](img/)

## 🛠️ Tecnologías

### Backend
- **Flask 2.3+** - Framework web principal
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de sesiones
- **Flask-WTF** - Formularios y protección CSRF
- **Werkzeug** - Seguridad de contraseñas
- **Pillow** - Procesamiento de imágenes

### Frontend
- **Bootstrap 5** - Framework CSS
- **Leaflet** - Mapas interactivos
- **Bootstrap Icons** - Iconografía
- **JavaScript ES6** - Interactividad

### Base de Datos
- **PostgreSQL** (Producción)
- **SQLite** (Desarrollo)

## 📦 Instalación

### Prerrequisitos

- Python 3.8 o superior
- PostgreSQL (para producción)
- Git

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/quadra.git
cd quadra
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
# Generar SECRET_KEY segura:
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Configurar base de datos

#### Opción A: SQLite (Desarrollo rápido)
```bash
# Las tablas se crean automáticamente al ejecutar
python run.py
```

#### Opción B: PostgreSQL (Recomendado para producción)

**Paso 1: Instalar PostgreSQL**
```bash
# Windows: Descargar desde https://www.postgresql.org/download/windows/
# O usar chocolatey:
choco install postgresql

# macOS:
brew install postgresql

# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib
```

**Paso 2: Crear base de datos y usuario**
```bash
# Conectar a PostgreSQL como superusuario
psql -U postgres

# Crear base de datos y usuario
CREATE DATABASE quadra_db;
CREATE USER quadra_user WITH PASSWORD 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON DATABASE quadra_db TO quadra_user;
\q
```

**Paso 3: Configurar DATABASE_URL en .env**
```bash
# Editar archivo .env y cambiar:
DATABASE_URL=postgresql://quadra_user:tu_contraseña_segura@localhost:5432/quadra_db
```

**Paso 4: Ejecutar migraciones**
```bash
# Inicializar migraciones (solo la primera vez)
flask db init

# Crear migración inicial
flask db migrate -m "Initial migration"

# Aplicar migraciones
flask db upgrade
```

**Paso 5: Verificar configuración**
```bash
# Ejecutar script de verificación
python setup_postgres.py
```

### 6. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 🎮 Uso

### Para Usuarios

1. **Explorar sin cuenta** - Ve el mapa principal con todos los puestos
2. **Registrarse** - Crea una cuenta para agregar puestos y reseñas
3. **Agregar puesto** - Sube un nuevo puesto con ubicación y foto
4. **Escribir reseñas** - Califica y comenta otros puestos
5. **Gestionar puestos** - Ve estadísticas de tus puestos agregados

### Para Desarrolladores

#### Estructura del Proyecto

```
quadra/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routes/          # Rutas y lógica de negocio
│   ├── templates/       # Plantillas HTML
│   ├── static/          # CSS, JS, imágenes
│   └── __init__.py      # Configuración de la app
├── migrations/          # Migraciones de base de datos
├── instance/           # Archivos de instancia (SQLite)
├── venv/               # Entorno virtual
├── requirements.txt    # Dependencias Python
├── run.py             # Punto de entrada
└── README.md          # Este archivo
```

#### Comandos Útiles

```bash
# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Ejecutar en modo debug
export FLASK_DEBUG=1
python run.py
```

## 🔒 Seguridad

La aplicación implementa múltiples capas de seguridad:

- ✅ **Protección CSRF** - Tokens en todos los formularios
- ✅ **Rate Limiting** - Prevención de ataques de fuerza bruta
- ✅ **Validación de entrada** - Sanitización de datos de usuario
- ✅ **Contraseñas seguras** - Hash con Werkzeug
- ✅ **Validación de archivos** - Tipos y tamaños permitidos
- ✅ **Prevención SQL Injection** - ORM SQLAlchemy

## 🚀 Despliegue

### Variables de Entorno Requeridas

```env
SECRET_KEY=tu_clave_secreta_super_larga
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/database
FLASK_ENV=production
```

### Plataformas Recomendadas

- **Heroku** - Fácil despliegue con PostgreSQL
- **DigitalOcean App Platform** - Escalable y económico
- **Railway** - Deployment automático desde Git

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork** el proyecto
2. **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

### Reportar Bugs

Por favor usa los [Issues de GitHub](https://github.com/tu-usuario/quadra/issues) para reportar bugs o solicitar nuevas características.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👥 Equipo

- **Desarrollador Principal** - [Tu Nombre](https://github.com/tu-usuario)

## 🙏 Agradecimientos

- [Flask Team](https://flask.palletsprojects.com/) por el excelente framework
- [Leaflet](https://leafletjs.com/) por los mapas interactivos
- [Bootstrap](https://getbootstrap.com/) por el framework CSS
- [OpenStreetMap](https://www.openstreetmap.org/) por los datos de mapas

---

<div align="center">

**⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/tu-usuario/quadra?style=social)](https://github.com/tu-usuario/quadra/stargazers)

</div>
