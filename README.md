## Dependencias y ejecución en localhost

Esta sección explica las dependencias necesarias y los pasos mínimos para ejecutar la aplicación en tu máquina (desarrollo / local).

### Requisitos
- Python 3.10 o superior
- pip
- (Opcional) PostgreSQL si quieres usar una base de datos real en vez de SQLite

Todas las dependencias Python están en `requirements.txt`.

---

### Pasos rápidos (Windows - PowerShell)

1) Clonar el repositorio y entrar en la carpeta:

```powershell
git clone https://github.com/angelaramiz/QUADRA.git
cd QUADRA
```

2) Crear y activar un entorno virtual (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4) Configurar variables de entorno básicas:

```powershell
# Copiar el ejemplo de configuración y editar app/.env
copy .\app\.env.example .\app\.env
# Edita .\app\.env y añade SECRET_KEY, DATABASE_URL u otras variables necesarias
```

5) Base de datos (opciones):

- Desarrollo rápido con SQLite: la app crea la base en `instance/` al arrancar.
- PostgreSQL (producción): instala PostgreSQL, crea la base y ajusta `DATABASE_URL` en `app/.env`. Luego aplica migraciones.

6) Ejecutar la aplicación (desde la raíz del proyecto):

```powershell
# Ejecutar con el script de inicio (recomendado)
python start.py

# Alternativa: ejecutar el módulo de la app
python -m app.run
```

La aplicación estará disponible en http://localhost:5000

---

### Migraciones (si usas PostgreSQL)

```powershell
# Activa tu entorno virtual y exporta FLASK_APP
.\venv\Scripts\Activate.ps1
$env:FLASK_APP = 'app.run'

# Aplicar migraciones (las migraciones están en app/migrations en este repo)
# -> usa --directory para indicar la carpeta de migraciones
python -m flask db upgrade --directory app/migrations
```

Si `flask` está en el PATH puedes usar:

```powershell
flask db upgrade --directory app/migrations
```

Nota: si la base de datos ya contiene las tablas y Alembic falla con "DuplicateTable",
marca las migraciones como aplicadas y luego aplica sólo las pendientes:

```powershell
$env:FLASK_APP = 'app.run'
python -m flask db stamp head --directory app/migrations
python -m flask db upgrade --directory app/migrations
```

---

### Notas rápidas
- Generar `SECRET_KEY` seguro:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

- Para desarrollo usa SQLite (archivo en `instance/quadra.db`). Para producción usa PostgreSQL y configura `DATABASE_URL`.
- `wsgi.py` y `Procfile` están en `.gitignore` y no se rastrean en el repo.

---

Si quieres que añada comandos de Docker o un ejemplo de `docker-compose`, dime y lo agrego.

---

### Generar `.env` (ejemplo y comandos)

Es importante crear `app/.env` antes de ejecutar la aplicación. Puedes partir de `.env.example` y rellenar los valores.

PowerShell — pasos rápidos:

```powershell
# Copiar el archivo de ejemplo
copy .\ .env.example .\app\.env

# Generar una SECRET_KEY segura y ponerla en el .env (muestra por pantalla)
python -c "import secrets; print(secrets.token_hex(32))"

# Edita app\.env con tu editor y reemplaza SECRET_KEY, DATABASE_URL, etc.
notepad .\app\.env
```

Contenido mínimo recomendado en `app/.env` para desarrollo (SQLite):

```env
SECRET_KEY=<tu_secret_key_generada>
FLASK_ENV=development
FLASK_DEBUG=False
DATABASE_URL=sqlite:///instance/quadra.db
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216
```

Ejemplo mínimo para producción con PostgreSQL:

```env
SECRET_KEY=<tu_secret_key_generada>
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://quadra_user:tu_password@localhost:5432/quadra_db
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216
```

Consejo: nunca subas `app/.env` al repositorio; mantenlo en `.gitignore`.
