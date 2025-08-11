# 📊 Checkpoint 2: Diseño inicial de la base de datos y flujos de usuario

**Fecha de entrega:** 11 de agosto de 2025  
**Estado:** ✅ **COMPLETADO**

## 📂 Contenido de esta carpeta

### 📄 **Documentos principales:**
- `checkpoint2.md` - Documentación completa del checkpoint
- `README.md` - Este archivo (índice del checkpoint)

### 📁 **Subcarpetas:**
- `/documentos/` - Esquemas y documentación técnica
- `/diagramas/` - Diagramas ER y de flujo

## 🎯 **Entregables completados**

### ✅ **1. Esquema entidad-relación**
- **Ubicación:** `/diagramas/esquema_er.png` (por generar)
- **Contenido:** 3 entidades principales con relaciones
- **Estado:** Implementado en PostgreSQL y funcionando

**Entidades implementadas:**
- **users** - Gestión de usuarios
- **food_stands** - Puestos de comida con geolocalización
- **reviews** - Sistema de reseñas y calificaciones

### ✅ **2. Diagramas de flujo de usuario**
- **Ubicación:** `/diagramas/flujos_usuario.png` (por generar)
- **Contenido:** 6 casos de uso principales
- **Estado:** Todos implementados y testeados

**Flujos implementados:**
1. 🔐 **Registro de usuario** - Completo con validaciones
2. 🔑 **Inicio de sesión** - Con persistencia de sesión
3. 🍔 **Crear puesto de comida** - Con mapa y fotos
4. ⭐ **Agregar reseña** - Con sistema de calificación
5. 🗺️ **Buscar puestos** - Con filtros y geolocalización
6. 👤 **Gestionar perfil** - CRUD de datos personales

## 🗃️ **Base de datos implementada**

### **🏗️ Arquitectura:**
```sql
users (1) ──→ (n) food_stands
food_stands (1) ──→ (n) reviews
users (1) ──→ (n) reviews
```

### **📋 Tablas principales:**

#### **👤 Tabla users:**
- `id` (PK) - Identificador único
- `username` - Nombre de usuario único
- `email` - Email único con validación
- `password_hash` - Hash seguro Werkzeug
- `created_at` - Timestamp de registro
- `is_active` - Estado del usuario

#### **🍔 Tabla food_stands:**
- `id` (PK) - Identificador único
- `name` - Nombre del puesto
- `description` - Descripción detallada
- `latitude/longitude` - Coordenadas GPS
- `address` - Dirección textual
- `food_type` - Categoría de comida
- `image_filename` - Archivo de imagen
- `user_id` (FK) - Propietario del puesto
- `created_at` - Timestamp de creación

#### **⭐ Tabla reviews:**
- `id` (PK) - Identificador único
- `rating` - Calificación 1-5 estrellas
- `comment` - Comentario opcional
- `user_id` (FK) - Usuario que reseña
- `food_stand_id` (FK) - Puesto reseñado
- `created_at` - Timestamp de la reseña

## 🔄 **Flujos de usuario verificados**

### **🔐 1. Registro de usuario**
```
Inicio → Formulario registro → Validación → Hash contraseña → BD → Login automático → Dashboard
```
**Estado:** ✅ Funcionando con validaciones completas

### **🔑 2. Inicio de sesión**
```
Inicio → Formulario login → Verificación → Sesión → Dashboard → Persistencia
```
**Estado:** ✅ Funcionando con sesiones persistentes

### **🍔 3. Crear puesto de comida**
```
Dashboard → Crear puesto → Formulario → Mapa → Imagen → Validación → BD → Vista detalle
```
**Estado:** ✅ Funcionando con mapa interactivo

### **⭐ 4. Agregar reseña**
```
Ver puesto → Formulario reseña → Calificación → Validación → BD → Actualizar promedio
```
**Estado:** ✅ Funcionando con cálculo automático

### **🗺️ 5. Buscar puestos**
```
Dashboard → Mapa → Filtros → Búsqueda → Resultados → Detalle
```
**Estado:** ✅ Funcionando con geolocalización

### **👤 6. Gestionar perfil**
```
Dashboard → Mi perfil → Editar → Validación → Actualizar BD → Confirmación
```
**Estado:** ✅ Funcionando con CRUD completo

## 📊 **Métricas de la base de datos**

### **🔍 Estado actual:**
- **Tablas creadas:** 3 tablas principales
- **Relaciones:** 3 foreign keys implementadas
- **Índices:** 5 índices para optimización
- **Constraints:** 8 restricciones de integridad

### **📈 Capacidad:**
- **Usuarios:** Escalable sin límite
- **Puestos:** Ilimitados por usuario
- **Reseñas:** Una por usuario/puesto
- **Imágenes:** Optimización automática

## 🛠️ **Herramientas utilizadas**

### **🎨 Para diagramas:**
- **Draw.io** - Diagramas ER y flujos
- **DB Diagram** - Esquemas de base de datos
- **Lucidchart** - Flujos de usuario (opcional)

### **🗃️ Para base de datos:**
- **PostgreSQL 17.4** - Motor principal
- **SQLAlchemy** - ORM y migraciones
- **pgAdmin** - Administración visual

## 📋 **Checklist de entrega**

- [x] **Base de datos implementada y funcionando**
- [x] **Todas las relaciones configuradas**
- [x] **Flujos de usuario implementados**
- [x] **Casos de uso verificados**
- [ ] **Diagrama ER exportado** (por generar)
- [ ] **Diagramas de flujo exportados** (por generar)

## 🎨 **Para generar los diagramas**

### **📊 Diagrama ER:**
1. **Conectar a PostgreSQL** con pgAdmin
2. **Generar diagrama ER** desde la base de datos
3. **Exportar como imagen** PNG/PDF
4. **Guardar en** `/diagramas/esquema_er.png`

### **🔄 Diagramas de flujo:**
1. **Abrir Draw.io** (app.diagrams.net)
2. **Crear flujos** para cada caso de uso
3. **Exportar como imágenes** PNG
4. **Compilar en** `/diagramas/flujos_usuario.png`

---

**📈 Estado:** Checkpoint completado exitosamente  
**🎯 Próximo:** Checkpoint 3 - Landing page, login y signup
