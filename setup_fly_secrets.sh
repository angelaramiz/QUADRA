#!/bin/bash
# Script para configurar variables de entorno en Fly.io para QUADRA

echo "🚀 Configurando variables de entorno para QUADRA en Fly.io..."
echo ""

# Variables críticas
echo "📋 1. Configurando variables críticas..."
flyctl secrets set SECRET_KEY="7c0a56cf774752aa7c8c3a1f8bcfc48d806a77fee8b59e298d62dbb45420cad5"
flyctl secrets set DATABASE_URL="postgresql://postgres.dfouootxfxsvvpxoerth:CuentaHasta22@aws-0-us-east-2.pooler.supabase.com:5432/postgres"

# Configuración de Flask para producción
echo "🔧 2. Configurando Flask para producción..."
flyctl secrets set FLASK_ENV="production"
flyctl secrets set FLASK_DEBUG="False"

# Configuración de archivos
echo "📁 3. Configurando manejo de archivos..."
flyctl secrets set UPLOAD_FOLDER="app/static/uploads"
flyctl secrets set MAX_CONTENT_LENGTH="16777216"

# Configuración de mapas
echo "🗺️  4. Configurando parámetros del mapa..."
flyctl secrets set MAP_DEFAULT_LAT="19.4326"
flyctl secrets set MAP_DEFAULT_LNG="-99.1332"
flyctl secrets set MAP_DEFAULT_ZOOM="12"

# Configuración de seguridad
echo "🔒 5. Configurando seguridad..."
flyctl secrets set WTF_CSRF_TIME_LIMIT="3600"
flyctl secrets set SESSION_COOKIE_HTTPONLY="True"
flyctl secrets set SESSION_COOKIE_SECURE="True"
flyctl secrets set PERMANENT_SESSION_LIFETIME="86400"

echo ""
echo "✅ ¡Configuración completa!"
echo ""
echo "📝 Resumen de variables configuradas:"
echo "   - SECRET_KEY: Nueva clave para producción"
echo "   - DATABASE_URL: Supabase PostgreSQL"
echo "   - FLASK_ENV: production"
echo "   - FLASK_DEBUG: False"
echo "   - Variables de mapas y archivos"
echo "   - Configuraciones de seguridad"
echo ""
echo "🔍 Para verificar las variables configuradas:"
echo "   flyctl secrets list"
echo ""
echo "🚀 Para desplegar tu aplicación:"
echo "   flyctl deploy"
