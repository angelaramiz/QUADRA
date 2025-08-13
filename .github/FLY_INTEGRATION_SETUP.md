# 🔄 Auto-Deploy con Fly.io Integration

## ⚡ **Configuración rápida:**

### 1. **Conectar repositorio:**
```bash
# En tu terminal local
flyctl apps open quadra-app
# Ve a la sección "GitHub Integration"
```

### 2. **Configurar desde Fly.io Dashboard:**
1. Abre https://fly.io/dashboard
2. Selecciona tu app `quadra-app`
3. Ve a "GitHub Integration"
4. Conecta tu repositorio `angelaramiz/QUADRA`
5. Selecciona rama `main` para auto-deploy

### 3. **Configuración automática:**
- ✅ Fly.io detecta automáticamente el Dockerfile
- ✅ Deploy en cada push a main
- ✅ No necesita configuración adicional

## 🆚 **Comparación de opciones:**

| Característica | GitHub Actions | Fly.io Integration |
|----------------|----------------|--------------------|
| **Configuración** | Media | Fácil |
| **Control** | Total | Limitado |
| **Tests** | ✅ Sí | ❌ No |
| **Notificaciones** | ✅ Customizable | ✅ Básicas |
| **Rollback** | ✅ Manual | ✅ Automático |
| **Costo** | Gratis | Gratis |

## 🎯 **Recomendación:**

**Para QUADRA:** GitHub Actions (Opción 1)
- ✅ Más control sobre el proceso
- ✅ Puedes agregar tests fácilmente
- ✅ Notificaciones personalizadas
- ✅ Historial completo en GitHub
