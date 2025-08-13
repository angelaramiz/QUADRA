# Script PowerShell para configurar QUADRA en Fly.io desde cero

Write-Host "Configurando QUADRA en Fly.io..." -ForegroundColor Green

# Paso 1: Limpiar configuración anterior si existe
Write-Host "Limpiando configuración anterior..." -ForegroundColor Yellow
if (Test-Path "fly.toml") {
    Write-Host "   - Respaldando fly.toml existente..."
    Copy-Item "fly.toml" "fly.toml.backup"
}

# Paso 2: Inicializar aplicación Fly.io
Write-Host "Inicializando aplicación en Fly.io..." -ForegroundColor Yellow
flyctl apps create quadra-app --org personal

# Paso 3: Crear volumen para archivos estáticos
Write-Host "Creando volumen para archivos..." -ForegroundColor Yellow
flyctl volumes create quadra_storage --size 1 --region dfw

# Paso 4: Configurar variables de entorno
Write-Host "Configurando variables de entorno..." -ForegroundColor Yellow
flyctl secrets set SECRET_KEY="7c0a56cf774752aa7c8c3a1f8bcfc48d806a77fee8b59e298d62dbb45420cad5"
flyctl secrets set DATABASE_URL="postgresql://postgres.dfouootxfxsvvpxoerth:CuentaHasta22@aws-0-us-east-2.pooler.supabase.com:5432/postgres"
flyctl secrets set FLASK_ENV="production"
flyctl secrets set FLASK_DEBUG="False"
flyctl secrets set UPLOAD_FOLDER="app/static/uploads"
flyctl secrets set MAX_CONTENT_LENGTH="16777216"
flyctl secrets set MAP_DEFAULT_LAT="19.4326"
flyctl secrets set MAP_DEFAULT_LNG="-99.1332"
flyctl secrets set MAP_DEFAULT_ZOOM="12"
flyctl secrets set WTF_CSRF_TIME_LIMIT="3600"
flyctl secrets set SESSION_COOKIE_HTTPONLY="True"
flyctl secrets set SESSION_COOKIE_SECURE="True"
flyctl secrets set PERMANENT_SESSION_LIFETIME="86400"

# Paso 5: Desplegar aplicación
Write-Host "Desplegando aplicación..." -ForegroundColor Yellow
flyctl deploy

Write-Host ""
Write-Host "QUADRA configurado exitosamente en Fly.io!" -ForegroundColor Green
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Cyan
Write-Host "   flyctl status    - Ver estado de la app"
Write-Host "   flyctl logs      - Ver logs en tiempo real"
Write-Host "   flyctl open      - Abrir app en el navegador"
Write-Host "   flyctl ssh console - Conectar por SSH"
