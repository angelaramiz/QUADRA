# Deployment - QUADRA

Esta carpeta contiene archivos y scripts para el despliegue de QUADRA en Fly.io.

## ⚠️ **ADVERTENCIA DE SEGURIDAD**

**🔒 NUNCA subas credenciales reales al repositorio**

- Los archivos aquí contienen **SOLO PLANTILLAS** con valores de ejemplo
- Reemplaza todos los valores `YOUR_*_HERE` con tus credenciales reales
- Usa siempre `flyctl secrets set` para configurar variables sensibles
- Las credenciales reales deben mantenerse en tu entorno local únicamente

## 📁 **Archivos incluidos:**

### 🚀 **Scripts de configuración automática:**
- **`setup_fly_complete.ps1`** - Script PowerShell completo para configurar QUADRA en Fly.io
- **`setup_fly_complete.sh`** - Script Bash completo para configurar QUADRA en Fly.io
- **`setup_fly_secrets.ps1`** - Script PowerShell solo para configurar variables de entorno
- **`setup_fly_secrets.sh`** - Script Bash solo para configurar variables de entorno

### 📝 **Archivos de referencia:**
- **`fly_secrets_manual.txt`** - Lista de comandos para configurar variables manualmente
- **`fly.toml.backup`** - Respaldo de la configuración de Fly.io

## 🛠️ **Instrucciones de uso:**

### 1. **Configuración completa (recomendado):**
```powershell
# PowerShell
.\deployment\setup_fly_complete.ps1

# Bash
chmod +x deployment/setup_fly_complete.sh
./deployment/setup_fly_complete.sh
```

### 2. **Solo configurar variables de entorno:**
```powershell
# PowerShell
.\deployment\setup_fly_secrets.ps1

# Bash
chmod +x deployment/setup_fly_secrets.sh
./deployment/setup_fly_secrets.sh
```

### 3. **Configuración manual:**
Sigue los comandos en `fly_secrets_manual.txt`

## ✅ **Prerrequisitos:**
- Tener `flyctl` instalado y autenticado
- Estar en la raíz del proyecto QUADRA
- Tener credenciales de Supabase configuradas

## 🔗 **Enlaces útiles:**
- [Documentación de Fly.io](https://fly.io/docs/)
- [Guía de despliegue Flask](https://fly.io/docs/languages-and-frameworks/python/)
- [CLI de Fly.io](https://fly.io/docs/hands-on/install-flyctl/)
