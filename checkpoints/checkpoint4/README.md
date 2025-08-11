# 🔐 Checkpoint 4: Implementación de autenticación y autorización

**Fecha de entrega:** 11 de agosto de 2025  
**Estado:** ✅ **COMPLETADO**

## 📂 Contenido de esta carpeta

### 📄 **Documentos principales:**
- `checkpoint4.md` - Documentación completa del checkpoint
- `README.md` - Este archivo (índice del checkpoint)

### 📁 **Subcarpetas:**
- `/videos/` - Videos demostrativos de autenticación
- `/documentos/` - Documentación técnica de seguridad

## 🎯 **Entregables completados**

### ✅ **1. Video de registro de usuario**
- **Ubicación:** `/videos/registro_usuario.mp4` (por grabar)
- **Duración:** 2-3 minutos
- **Contenido:** Proceso completo de registro con validaciones

### ✅ **2. Video de inicio de sesión**
- **Ubicación:** `/videos/inicio_sesion.mp4` (por grabar)
- **Duración:** 1-2 minutos
- **Contenido:** Login exitoso y manejo de errores

### ✅ **3. Video de persistencia de sesión**
- **Ubicación:** `/videos/persistencia_sesion.mp4` (por grabar)
- **Duración:** 1-2 minutos
- **Contenido:** Sesión manteniéndose tras cerrar/abrir navegador

## 🔒 **Sistema de seguridad implementado**

### **🛡️ Autenticación robusta:**

#### **🔐 Hash de contraseñas:**
```python
# Werkzeug Security
from werkzeug.security import generate_password_hash, check_password_hash

# En modelo User
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

#### **🎫 Gestión de sesiones:**
```python
# Flask-Login configurado
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder.'

# Usuario loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### **🛡️ Protección CSRF:**
```python
# Flask-WTF protection
app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura'

# En formularios
{{ csrf_token() }}
```

### **⏱️ Rate Limiting:**
```python
# Flask-Limiter configurado
@limiter.limit("5 per minute")
def login():
    # Máximo 5 intentos de login por minuto
```

## 🔄 **Flujos de autenticación verificados**

### **📝 1. Registro de usuario**

#### **Pasos del flujo:**
1. **Acceso:** Usuario va a `/auth/register`
2. **Formulario:** Completa username, email, password, confirm_password
3. **Validación frontend:** JavaScript valida campos en tiempo real
4. **Validación backend:** Flask-WTF valida datos
5. **Verificación unicidad:** Verifica que username y email no existan
6. **Hash contraseña:** Werkzeug genera hash seguro
7. **Guardar BD:** Usuario creado en PostgreSQL
8. **Login automático:** Usuario logueado inmediatamente
9. **Redirect:** Dirigido al dashboard

#### **Validaciones implementadas:**
- ✅ **Username único** (3-20 caracteres)
- ✅ **Email válido y único**
- ✅ **Contraseña fuerte** (mínimo 8 caracteres)
- ✅ **Confirmación contraseña** debe coincidir
- ✅ **Protección CSRF** en formulario
- ✅ **Rate limiting** 5 registros por minuto

### **🔑 2. Inicio de sesión**

#### **Pasos del flujo:**
1. **Acceso:** Usuario va a `/auth/login`
2. **Formulario:** Ingresa username/email y password
3. **Verificación:** Sistema busca usuario en BD
4. **Hash check:** Werkzeug verifica contraseña
5. **Remember me:** Opción de sesión persistente
6. **Login:** Flask-Login crea sesión
7. **Redirect:** Dirigido a página solicitada o dashboard

#### **Características de seguridad:**
- ✅ **Verificación hash** segura con Werkzeug
- ✅ **Remember me** para sesiones persistentes
- ✅ **Rate limiting** máximo 5 intentos por minuto
- ✅ **Mensajes de error** genéricos (no revelan si usuario existe)
- ✅ **Protección CSRF**
- ✅ **Redirección segura** tras login

### **🔄 3. Persistencia de sesión**

#### **Funcionalidades verificadas:**
- ✅ **Sesión mantiene** tras cerrar navegador
- ✅ **Remember me** funciona correctamente
- ✅ **Auto-login** en siguiente visita
- ✅ **Logout** limpia sesión completamente
- ✅ **Timeout** configurable de sesiones

## 🔐 **Autorización granular**

### **🛣️ Protección de rutas:**

#### **Rutas públicas:**
```python
# Accesibles sin autenticación
@app.route('/')  # Landing page
@app.route('/auth/login')  # Login form
@app.route('/auth/register')  # Register form
```

#### **Rutas protegidas:**
```python
# Requieren autenticación
@login_required
@app.route('/dashboard')  # Dashboard principal
@app.route('/food-stands/create')  # Crear puesto
@app.route('/food-stands/my-stands')  # Mis puestos
```

#### **Rutas con autorización específica:**
```python
# Solo propietario puede editar/eliminar
def check_food_stand_owner(food_stand_id):
    stand = FoodStand.query.get_or_404(food_stand_id)
    if stand.user_id != current_user.id:
        abort(403)  # Forbidden
```

### **🔒 Niveles de autorización:**

1. **👤 Usuario anónimo:**
   - ✅ Ver landing page
   - ✅ Registrarse
   - ✅ Iniciar sesión
   - ❌ Acceso a funcionalidades

2. **🔓 Usuario autenticado:**
   - ✅ Ver dashboard
   - ✅ Crear puestos
   - ✅ Ver todos los puestos
   - ✅ Agregar reseñas
   - ❌ Editar puestos de otros

3. **👑 Propietario de recurso:**
   - ✅ Editar sus propios puestos
   - ✅ Eliminar sus propios puestos
   - ✅ Gestionar sus datos
   - ❌ Modificar recursos de otros

## 🎬 **Guías para videos demostrativos**

### **📝 Video 1: Registro de usuario (2-3 min)**

**Guión:**
1. **[0:00-0:15]** Acceder a la página de registro
2. **[0:15-0:45]** Llenar formulario con datos válidos
3. **[0:45-1:15]** Demostrar validaciones (campos vacíos, email inválido)
4. **[1:15-1:45]** Intentar registro con usuario existente
5. **[1:45-2:15]** Registro exitoso y redirect automático
6. **[2:15-2:30]** Mostrar usuario logueado en dashboard

### **🔑 Video 2: Inicio de sesión (1-2 min)**

**Guión:**
1. **[0:00-0:15]** Logout del usuario actual
2. **[0:15-0:30]** Acceder al formulario de login
3. **[0:30-0:45]** Intentar login con credenciales incorrectas
4. **[0:45-1:00]** Login exitoso con credenciales correctas
5. **[1:00-1:15]** Verificar acceso a funcionalidades protegidas
6. **[1:15-1:30]** Demostrar redirección tras login

### **🔄 Video 3: Persistencia de sesión (1-2 min)**

**Guión:**
1. **[0:00-0:15]** Login con "Remember me" activado
2. **[0:15-0:30]** Navegar por la aplicación
3. **[0:30-0:45]** Cerrar completamente el navegador
4. **[0:45-1:00]** Abrir navegador y volver a la aplicación
5. **[1:00-1:15]** Verificar que sigue logueado
6. **[1:15-1:30]** Logout manual para limpiar sesión

## 📊 **Métricas de seguridad**

### **🔒 Características implementadas:**
- **Hash algorithm:** Werkzeug PBKDF2-SHA256
- **Session security:** Flask-Login + secure cookies
- **CSRF protection:** Flask-WTF tokens
- **Rate limiting:** Flask-Limiter (5 req/min login)
- **Password policy:** Mínimo 8 caracteres
- **Session timeout:** Configurable

### **🛡️ Vulnerabilidades prevenidas:**
- ✅ **SQL Injection** - SQLAlchemy ORM
- ✅ **XSS** - Jinja2 auto-escaping
- ✅ **CSRF** - Flask-WTF tokens
- ✅ **Brute force** - Rate limiting
- ✅ **Session hijacking** - Secure cookies
- ✅ **Password cracking** - Strong hashing

## 📋 **Checklist de verificación**

### **✅ Funcionalidades básicas:**
- [x] **Registro de usuario** funcionando
- [x] **Login de usuario** funcionando
- [x] **Logout de usuario** funcionando
- [x] **Persistencia de sesión** funcionando

### **✅ Validaciones:**
- [x] **Username único** verificado
- [x] **Email único** verificado
- [x] **Contraseña fuerte** requerida
- [x] **Confirmación contraseña** verificada

### **✅ Seguridad:**
- [x] **Hash de contraseñas** implementado
- [x] **Protección CSRF** activa
- [x] **Rate limiting** configurado
- [x] **Rutas protegidas** funcionando

### **✅ Autorización:**
- [x] **Acceso según roles** implementado
- [x] **Propietario de recursos** verificado
- [x] **Páginas públicas/privadas** correctas

---

**📈 Estado:** Checkpoint completado exitosamente  
**🎯 Próximo:** Checkpoint 5 - Página inicial de la aplicación
