# Scripts de QUADRA

Esta carpeta contiene scripts de utilidad para la configuración y mantenimiento de la base de datos.

## 📋 **Scripts disponibles:**

### 🔧 **Configuración inicial:**
- **`init_supabase.py`** - Inicializa la base de datos Supabase con las tablas necesarias
- **`migrate_data_to_supabase.py`** - Migra datos existentes de SQLite a Supabase
- **`verify_supabase.py`** - Verifica la conexión y datos en Supabase

### 🔐 **Actualizaciones:**
- **`update_database_for_password_reset.py`** - Agrega campos necesarios para recuperación de contraseña

## 🚀 **Uso:**

```bash
# Desde la raíz del proyecto
python scripts/init_supabase.py
python scripts/verify_supabase.py
python scripts/migrate_data_to_supabase.py
python scripts/update_database_for_password_reset.py
```

## ⚠️ **Notas importantes:**
- Ejecutar siempre desde la raíz del proyecto
- Asegúrate de tener configurado el archivo `.env` con las credenciales de Supabase
- Los scripts son seguros para ejecutar múltiples veces
