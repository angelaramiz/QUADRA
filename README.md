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

<div align="center">
  <img src="app/static/images/logo.svg" alt="QUADRA Logo" width="300">
</div>

# 🍕 QUADRA - Plataforma de Puestos de Comida

[![Deployed on Fly.io](https://img.shields.io/badge/Deployed-Fly.io-blueviolet)](https://quadra-app.fly.dev)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://quadra-app.fly.dev)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-blue)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791)](https://supabase.com/)

**QUADRA** es una aplicación web desarrollada con Flask que permite a los usuarios descubrir, registrar y calificar puestos de comida mediante un sistema de mapas interactivo con geolocalización automática.

🌐 **[VER DEMO EN VIVO](https://quadra-app.fly.dev)** 🌐

## 🚀 **Características principales:**

- 🗺️ **Mapa interactivo** con geolocalización automática
- 📍 **Registro de puestos** de comida con ubicación GPS
- ⭐ **Sistema de reseñas** y calificaciones
- 🔐 **Autenticación completa** con recuperación de contraseña
- 📱 **Diseño responsive** optimizado para móviles
- ☁️ **Base de datos Supabase** PostgreSQL en la nube
- 🚀 **Desplegado en Fly.io** con HTTPS

## 🏗️ **Estructura del proyecto:**

```
QUADRA/
├── 📁 app/                    # Aplicación Flask principal
│   ├── 📁 models/            # Modelos de base de datos
│   ├── 📁 routes/            # Rutas y controladores
│   ├── 📁 static/            # Archivos estáticos (CSS, JS, imágenes)
│   ├── 📁 templates/         # Plantillas HTML
│   └── 📁 migrations/        # Migraciones de base de datos
├── 📁 scripts/               # Scripts de utilidad y configuración
├── 📁 deployment/            # Archivos para despliegue en Fly.io
├── 📁 docs/                  # Documentación técnica
├── 📁 checkpoints/           # Documentación de desarrollo
├── 🐳 Dockerfile            # Configuración de Docker
├── ✈️ fly.toml              # Configuración de Fly.io
├── 📋 requirements.txt      # Dependencias de Python
├── 🚀 start.py              # Punto de entrada principal
└── 🌐 wsgi.py               # Entrada para servidor WSGI
```

## 🛠️ **Tecnologías utilizadas:**

### Backend:
- **Flask** - Framework web de Python
- **SQLAlchemy** - ORM para base de datos
- **Flask-Login** - Gestión de sesiones
- **Flask-WTF** - Formularios y validación
- **Supabase PostgreSQL** - Base de datos en la nube

### Frontend:
- **Bootstrap 5** - Framework CSS
- **Leaflet.js** - Mapas interactivos
- **JavaScript ES6+** - Funcionalidades del cliente
- **Geolocation API** - Detección automática de ubicación

### Despliegue:
- **Fly.io** - Plataforma de hosting
- **Docker** - Contenedorización
- **Gunicorn** - Servidor WSGI para producción

## 🚀 **Instalación y configuración:**

### 1. **Clonar el repositorio:**
```bash
git clone https://github.com/angelaramiz/QUADRA.git
cd QUADRA
```

### 2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

### 4. **Configurar variables de entorno:**
```bash
# Crear archivo .env en la carpeta app/
cp app/.env.example app/.env
# Editar con tus credenciales de Supabase
```

### 5. **Inicializar base de datos:**
```bash
python scripts/init_supabase.py
```

### 6. **Ejecutar la aplicación:**
```bash
python start.py
```

La aplicación estará disponible en `http://localhost:5000`

## ☁️ **Despliegue en Fly.io:**

### Configuración automática:
```bash
# PowerShell
.\deployment\setup_fly_complete.ps1

# Bash
./deployment/setup_fly_complete.sh
```

### Configuración manual:
Consulta los archivos en la carpeta `deployment/` para instrucciones detalladas.

## 📚 **Documentación:**

- **[Scripts](scripts/README.md)** - Documentación de scripts de utilidad
- **[Deployment](deployment/README.md)** - Guías de despliegue
- **[Docs](docs/README.md)** - Documentación técnica de features

## 🔐 **Funcionalidades de seguridad:**

- ✅ Autenticación con hash de contraseñas
- ✅ Recuperación de contraseña por email
- ✅ Protección CSRF
- ✅ Rate limiting en login
- ✅ Cookies seguras en producción
- ✅ Validación de formularios

## 🗺️ **Funcionalidades del mapa:**

- ✅ Geolocalización automática
- ✅ Marcadores personalizados
- ✅ Información emergente (popups)
- ✅ Búsqueda por ubicación
- ✅ Diseño responsive
- ✅ Manejo de errores de ubicación

## 🎯 **Estado del proyecto:**

**🟢 Producción** - La aplicación está desplegada y funcionando en:
- **URL:** [https://quadra-app.fly.dev](https://quadra-app.fly.dev)
- **Estado:** Activo ✅
- **Base de datos:** Supabase PostgreSQL ✅
- **Última actualización:** Agosto 2025

## 👥 **Contribuciones:**

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 **Licencia:**

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 **Contacto:**

- **Desarrollador:** Angel Aramiz
- **Email:** angelaramiz22@gmail.com
- **Proyecto:** [https://github.com/angelaramiz/QUADRA](https://github.com/angelaramiz/QUADRA)

---

⭐ **¡Dale una estrella al proyecto si te ha sido útil!** es una aplicación web desarrollada con Flask que permite a los usuarios descubrir, agregar y calificar puestos de comida callejera. Los usuarios pueden compartir ubicaciones georeferenciadas, subir fotos, escribir reseñas y encontrar los mejores sabores de su ciudad.

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
# Las variables de entorno están en app/.env
# Copiar archivo de ejemplo desde app/
cp app/.env.example app/.env

# Editar app/.env con tus configuraciones
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

**Paso 3: Configurar DATABASE_URL en app/.env**
```bash
# Editar archivo app/.env y cambiar:
DATABASE_URL=postgresql://quadra_user:tu_contraseña_segura@localhost:5432/quadra_db
```

**Paso 4: Ejecutar migraciones**
```bash
# Cambiar al directorio de la aplicación
cd app

# Inicializar migraciones (solo la primera vez)
flask db init

# Crear migración inicial
flask db migrate -m "Initial migration"

# Aplicar migraciones
flask db upgrade

# Volver al directorio raíz
cd ..
```

**Paso 5: Verificar configuración**
```bash
# Ejecutar script de verificación desde app/
cd app
python setup_postgres.py
cd ..
```

### 6. Ejecutar la aplicación

```bash
# Método recomendado: Desde la raíz del proyecto
python -m app.run

# Método alternativo: Usando el script de inicio
python start.py

# Para desarrollo dentro de la carpeta app (requiere configuración adicional)
cd app
python run.py
```

**⚠️ Nota importante:** Se recomienda ejecutar la aplicación desde el directorio raíz del proyecto para evitar problemas de importación de módulos.

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
QUADRA/
├── app/                    # 📁 Aplicación principal
│   ├── models/            #   🗃️ Modelos de base de datos
│   ├── routes/            #   🚏 Rutas y lógica de negocio
│   ├── templates/         #   📄 Plantillas HTML
│   ├── static/            #   🎨 CSS, JS, imágenes
│   ├── migrations/        #   🔄 Migraciones de base de datos
│   ├── instance/          #   💾 Archivos de instancia (SQLite)
│   ├── .env               #   ⚙️ Variables de entorno
│   ├── .env.example       #   📋 Ejemplo de configuración
│   ├── run.py             #   🚀 Ejecutor interno de la app
│   ├── setup_postgres.py  #   🐘 Configurador PostgreSQL
│   └── __init__.py        #   📦 Configuración de la app
├── checkpoints/           # 📚 Documentación académica
├── img/                   # 🖼️ Imágenes del proyecto
├── venv/                  # 🐍 Entorno virtual Python
├── .gitignore             # 🚫 Archivos ignorados por Git
├── LICENSE                # 📜 Licencia MIT
├── README.md              # 📖 Este archivo
├── requirements.txt       # 📋 Dependencias Python
├── run.py                 # 🎬 Punto de entrada principal
└── setup_postgres.py      # 🔧 Script de configuración PostgreSQL
```

#### Comandos Útiles

```bash
# Ejecutar la aplicación
python -m app.run
# O: cd app && python run.py

# Configurar PostgreSQL
cd app && python setup_postgres.py

# Crear nueva migración
cd app
flask db migrate -m "Descripción del cambio"
flask db upgrade
cd ..

# Ejecutar en modo debug
export FLASK_DEBUG=1
python -m app.run

# Instalar dependencias
pip install -r requirements.txt

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
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
