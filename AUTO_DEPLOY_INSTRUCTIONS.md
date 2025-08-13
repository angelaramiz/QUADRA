# 🚀 INSTRUCCIONES PARA HABILITAR AUTO-DEPLOY

## ⚡ **Opción 1: GitHub Actions (Recomendada)**

### 📋 **Pasos a seguir:**

#### 1. **Instalar flyctl (si no lo tienes):**
```powershell
# PowerShell (Windows)
iwr https://fly.io/install.ps1 -useb | iex
```

#### 2. **Obtener token de Fly.io con permisos de deploy:**
```bash
flyctl tokens create deploy
```

**⚠️ IMPORTANTE:** Usa `flyctl tokens create deploy` en lugar de `flyctl auth token` para tener permisos suficientes.

#### 3. **Configurar secret en GitHub:**
1. Ve a: https://github.com/angelaramiz/QUADRA/settings/secrets/actions
2. Click "New repository secret" (o "Update" si ya existe)
3. Name: `FLY_API_TOKEN`
4. Value: [Pegar el token del paso 2 - DEBE EMPEZAR CON "FlyV1"]
5. Click "Add secret"

#### 4. **¡Listo! 🎉**
- El archivo `.github/workflows/deploy.yml` ya está creado
- Próximo push a `main` = auto-deploy automático

---

## ⚡ **Opción 2: Fly.io Integration (Más simple)**

### 📋 **Pasos alternativos:**

1. **Abrir dashboard de Fly.io:**
   - Ve a: https://fly.io/dashboard
   - Selecciona tu app `quadra-app`

2. **Conectar GitHub:**
   - Click en "GitHub Integration"
   - Autoriza acceso a tu repositorio
   - Selecciona `angelaramiz/QUADRA`
   - Rama: `main`

3. **¡Automático! 🎉**
   - Deploy en cada push a main
   - Sin configuración adicional

---

## 🔄 **Estado actual:**

✅ **Problema de producción RESUELTO**
- Error 500 en /dashboard corregido manualmente
- App funcionando: https://quadra-app.fly.dev

🔧 **Auto-deploy pendiente:**
1. ❌ Token actual no tiene permisos suficientes  
2. ✅ Nuevo token con permisos creado: `FlyV1 fm2_...`
3. 🔧 Necesitas actualizar FLY_API_TOKEN en GitHub Secrets
4. ✅ Archivo GitHub Actions ya configurado

✅ **Una vez actualizado el token:**
- Push a `main` → Deploy automático funcionará
- App se actualizará automáticamente en: https://quadra-app.fly.dev

---

## 🎯 **Mi recomendación:**

**Usa GitHub Actions** porque:
- ✅ Más control sobre el proceso
- ✅ Puedes agregar tests
- ✅ Mejor logging y notificaciones
- ✅ Rollback más fácil si algo falla

¿Quieres que te ayude a configurar alguna de estas opciones?
