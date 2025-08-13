# Script PowerShell para configurar variables de entorno en Fly.io para QUADRA

Write-Host "Configurando variables de entorno para QUADRA en Fly.io..." -ForegroundColor Green
Write-Host ""

# Variables críticas
Write-Host "1. Configurando variables críticas..." -ForegroundColor Yellow
flyctl secrets set SECRET_KEY="7c0a56cf774752aa7c8c3a1f8bcfc48d806a77fee8b59e298d62dbb45420cad5"
flyctl secrets set DATABASE_URL="postgresql://postgres.dfouootxfxsvvpxoerth:CuentaHasta22@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

# Configuración de Flask para producción
Write-Host "2. Configurando Flask para producción..." -ForegroundColor Yellow
flyctl secrets set FLASK_ENV="production"
flyctl secrets set FLASK_DEBUG="False"

# Configuración de archivos
Write-Host "3. Configurando manejo de archivos..." -ForegroundColor Yellow
flyctl secrets set UPLOAD_FOLDER="app/static/uploads"
flyctl secrets set MAX_CONTENT_LENGTH="16777216"

# Configuración de mapas
Write-Host "4. Configurando parámetros del mapa..." -ForegroundColor Yellow
flyctl secrets set MAP_DEFAULT_LAT="19.4326"
flyctl secrets set MAP_DEFAULT_LNG="-99.1332"
flyctl secrets set MAP_DEFAULT_ZOOM="12"

# Configuración de seguridad
Write-Host "5. Configurando seguridad..." -ForegroundColor Yellow
flyctl secrets set WTF_CSRF_TIME_LIMIT="3600"
flyctl secrets set SESSION_COOKIE_HTTPONLY="True"
flyctl secrets set SESSION_COOKIE_SECURE="True"
flyctl secrets set PERMANENT_SESSION_LIFETIME="86400"

Write-Host ""
Write-Host "Configuración completa!" -ForegroundColor Green
Write-Host ""
Write-Host "Resumen de variables configuradas:" -ForegroundColor Cyan
Write-Host "   - SECRET_KEY: Nueva clave para producción"
Write-Host "   - DATABASE_URL: Supabase PostgreSQL"
Write-Host "   - FLASK_ENV: production"
Write-Host "   - FLASK_DEBUG: False"
Write-Host "   - Variables de mapas y archivos"
Write-Host "   - Configuraciones de seguridad"
Write-Host ""
Write-Host "Para verificar las variables configuradas:" -ForegroundColor Cyan
Write-Host "   flyctl secrets list"
Write-Host ""
Write-Host "Para desplegar tu aplicación:" -ForegroundColor Cyan
Write-Host "   flyctl deploy"
