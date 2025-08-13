# 🔐 Configuración de GitHub Actions para Auto-Deploy

## 📋 **Pasos para habilitar auto-deploy:**

### 1. **Obtener token de Fly.io:**
```bash
# Generar token de autenticación
flyctl auth token
```

### 2. **Configurar secret en GitHub:**
1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Name: `FLY_API_TOKEN`
5. Value: [El token que obtuviste del paso 1]

### 3. **Verificar configuración:**
- El archivo `.github/workflows/deploy.yml` ya está creado
- Se ejecutará automáticamente en cada push a `main`
- Solo despliega si todos los tests pasan

## 🔄 **Flujo de trabajo:**

```
📝 git push origin main
     ↓
🧪 GitHub Actions ejecuta tests
     ↓
✅ Tests exitosos
     ↓
🚀 Auto-deploy a Fly.io
     ↓
🌐 App actualizada en quadra-app.fly.dev
```

## ⚙️ **Configuración adicional (opcional):**

### Despliegue por ambientes:
```yaml
# Para staging en rama develop
on:
  push:
    branches: [ main, develop ]

# Deploy a diferentes apps según la rama
- name: Deploy to staging
  if: github.ref == 'refs/heads/develop'
  run: flyctl deploy --app quadra-staging

- name: Deploy to production  
  if: github.ref == 'refs/heads/main'
  run: flyctl deploy --app quadra-app
```

### Notificaciones Slack/Discord:
```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🛡️ **Seguridad:**
- ✅ Token FLY_API_TOKEN está en GitHub Secrets
- ✅ No se exponen credenciales en el código
- ✅ Deploy solo en rama main
- ✅ Tests ejecutados antes del deploy

## 📞 **Comandos útiles:**

```bash
# Ver status del último deploy
flyctl status

# Ver logs del deploy
flyctl logs

# Rollback si algo sale mal
flyctl releases list
flyctl rollback [version]
```
