# 📊 Checkpoint 2: Diseño inicial de la base de datos y flujos de usuario

**Fecha de entrega:** [Pendiente]  
**Estado:** ✅ COMPLETADO

---

## 📑 Entregables

### Entregable 1: Esquema entidad-relación de la base de datos ✅

**Descripción:** Esquema entidad-relación de la base de datos que utilizará la aplicación. Este esquema deberá subirse en la plataforma en el apartado indicado, y adicionalmente, se deberá subir al repositorio en una carpeta llamada "documentation/db".

**Estado:** ✅ **COMPLETADO**

**Ubicación:** 
- **Repositorio:** `/documentation/db/` 
- **Plataforma:** [Subir en apartado indicado]

### Entregable 2: Diagramas de flujo de casos de uso ✅

**Descripción:** Diagramas de flujo de los distintos casos de uso que los usuarios podrán ejecutar en la plataforma. Estos diagramas deberán subir al repositorio sin comprimirse en carpeta.

**Estado:** ✅ **COMPLETADO**

**Ubicación:** `/documentation/flowcharts/`

---

## 🗃️ Diseño de Base de Datos

### 📋 **Esquema Entidad-Relación**

```mermaid
erDiagram
    USERS ||--o{ FOOD_STANDS : creates
    USERS ||--o{ REVIEWS : writes
    FOOD_STANDS ||--o{ REVIEWS : receives
    
    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    FOOD_STANDS {
        int id PK
        string name
        text description
        decimal latitude
        decimal longitude
        string address
        string image_filename
        int user_id FK
        datetime created_at
        datetime updated_at
        boolean is_active
    }
    
    REVIEWS {
        int id PK
        int rating
        text comment
        int user_id FK
        int food_stand_id FK
        datetime created_at
        datetime updated_at
    }
```

### 🔗 **Relaciones**

1. **USERS → FOOD_STANDS** (1:N)
   - Un usuario puede crear múltiples puestos de comida
   - Cada puesto pertenece a un único usuario

2. **USERS → REVIEWS** (1:N)
   - Un usuario puede escribir múltiples reseñas
   - Cada reseña es escrita por un único usuario

3. **FOOD_STANDS → REVIEWS** (1:N)
   - Un puesto puede recibir múltiples reseñas
   - Cada reseña pertenece a un único puesto

### 📊 **Especificaciones de Tablas**

#### 👤 **USERS**
| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único |
| username | VARCHAR(80) | UNIQUE, NOT NULL | Nombre de usuario |
| email | VARCHAR(120) | UNIQUE, NOT NULL | Correo electrónico |
| password_hash | VARCHAR(255) | NOT NULL | Contraseña hasheada |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de registro |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Última actualización |
| is_active | BOOLEAN | DEFAULT TRUE | Usuario activo |

#### 🏪 **FOOD_STANDS**
| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único |
| name | VARCHAR(100) | NOT NULL | Nombre del puesto |
| description | TEXT | | Descripción del puesto |
| latitude | DECIMAL(10,8) | NOT NULL | Coordenada latitud |
| longitude | DECIMAL(11,8) | NOT NULL | Coordenada longitud |
| address | VARCHAR(200) | | Dirección física |
| image_filename | VARCHAR(100) | | Nombre del archivo de imagen |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Propietario del puesto |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Última actualización |
| is_active | BOOLEAN | DEFAULT TRUE | Puesto activo |

#### ⭐ **REVIEWS**
| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Identificador único |
| rating | INTEGER | NOT NULL, CHECK (1-5) | Calificación 1-5 estrellas |
| comment | TEXT | | Comentario de la reseña |
| user_id | INTEGER | FOREIGN KEY, NOT NULL | Autor de la reseña |
| food_stand_id | INTEGER | FOREIGN KEY, NOT NULL | Puesto reseñado |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Última actualización |

---

## 🔄 Diagramas de Flujo de Casos de Uso

### 1. **Flujo de Registro de Usuario**

```mermaid
flowchart TD
    A[Usuario accede al sitio] --> B{¿Tiene cuenta?}
    B -->|No| C[Clic en 'Registrarse']
    C --> D[Llenar formulario de registro]
    D --> E[Enviar formulario]
    E --> F{¿Datos válidos?}
    F -->|No| G[Mostrar errores] --> D
    F -->|Sí| H[Crear cuenta en BD]
    H --> I[Iniciar sesión automáticamente]
    I --> J[Redirigir a dashboard]
    B -->|Sí| K[Ir a login]
```

### 2. **Flujo de Inicio de Sesión**

```mermaid
flowchart TD
    A[Usuario en landing page] --> B[Clic en 'Iniciar Sesión']
    B --> C[Mostrar formulario de login]
    C --> D[Ingresar credenciales]
    D --> E[Enviar formulario]
    E --> F{¿Credenciales válidas?}
    F -->|No| G[Mostrar error] --> C
    F -->|Sí| H[Crear sesión]
    H --> I[Redirigir a dashboard]
    I --> J[Mostrar contenido personalizado]
```

### 3. **Flujo de Creación de Puesto**

```mermaid
flowchart TD
    A[Usuario autenticado] --> B[Clic en 'Agregar Puesto']
    B --> C[Mostrar formulario]
    C --> D[Llenar información del puesto]
    D --> E[Seleccionar ubicación en mapa]
    E --> F[Subir imagen del puesto]
    F --> G[Enviar formulario]
    G --> H{¿Datos válidos?}
    H -->|No| I[Mostrar errores] --> C
    H -->|Sí| J[Guardar en BD]
    J --> K[Procesar imagen]
    K --> L[Mostrar puesto creado]
    L --> M[Redirigir a 'Mis Puestos']
```

### 4. **Flujo de Búsqueda y Visualización**

```mermaid
flowchart TD
    A[Usuario en página principal] --> B[Ver mapa con puestos]
    B --> C{¿Desea filtrar?}
    C -->|Sí| D[Usar filtros de búsqueda]
    D --> E[Actualizar mapa]
    E --> F[Mostrar resultados filtrados]
    C -->|No| F
    F --> G[Clic en marcador del mapa]
    G --> H[Mostrar popup con información]
    H --> I{¿Ver detalles?}
    I -->|Sí| J[Ir a página de detalle]
    I -->|No| K[Continuar navegando]
    J --> L[Mostrar información completa]
    L --> M[Ver reseñas y calificaciones]
```

### 5. **Flujo de Creación de Reseña**

```mermaid
flowchart TD
    A[Usuario en detalle de puesto] --> B{¿Está autenticado?}
    B -->|No| C[Mostrar botón de login]
    C --> D[Redirigir a login]
    B -->|Sí| E{¿Es dueño del puesto?}
    E -->|Sí| F[No puede reseñar su propio puesto]
    E -->|No| G[Mostrar formulario de reseña]
    G --> H[Seleccionar calificación (1-5)]
    H --> I[Escribir comentario opcional]
    I --> J[Enviar reseña]
    J --> K{¿Datos válidos?}
    K -->|No| L[Mostrar errores] --> G
    K -->|Sí| M[Guardar reseña en BD]
    M --> N[Actualizar promedio de calificación]
    N --> O[Mostrar reseña en la página]
    O --> P[Actualizar estadísticas del puesto]
```

### 6. **Flujo de Gestión de Puestos del Usuario**

```mermaid
flowchart TD
    A[Usuario autenticado] --> B[Ir a 'Mis Puestos']
    B --> C[Mostrar lista de puestos del usuario]
    C --> D{¿Qué acción desea?}
    D -->|Ver| E[Ir a detalle del puesto]
    D -->|Editar| F[Mostrar formulario de edición]
    D -->|Eliminar| G[Confirmar eliminación]
    F --> H[Actualizar información]
    H --> I[Guardar cambios en BD]
    G --> J{¿Confirmar?}
    J -->|Sí| K[Marcar como inactivo en BD]
    J -->|No| C
    I --> C
    K --> C
    E --> L[Ver estadísticas y reseñas]
```

---

## 🎯 **Casos de Uso Principales**

### 👤 **Gestión de Usuarios**
1. **Registro de usuario** - Crear nueva cuenta
2. **Inicio de sesión** - Autenticación de usuario
3. **Cierre de sesión** - Terminar sesión
4. **Recuperación de contraseña** - (Futuro)

### 🏪 **Gestión de Puestos de Comida**
1. **Crear puesto** - Agregar nuevo puesto con ubicación
2. **Ver puestos** - Visualizar en mapa y lista
3. **Editar puesto** - Modificar información propia
4. **Eliminar puesto** - Desactivar puesto propio
5. **Buscar puestos** - Filtrar por criterios

### ⭐ **Sistema de Reseñas**
1. **Escribir reseña** - Calificar y comentar
2. **Ver reseñas** - Leer opiniones de otros usuarios
3. **Calcular promedio** - Mostrar calificación general

### 🗺️ **Navegación y Búsqueda**
1. **Ver mapa interactivo** - Explorar puestos cercanos
2. **Usar geolocalización** - Encontrar puestos cerca
3. **Filtrar resultados** - Búsqueda avanzada
4. **Ver detalles** - Información completa del puesto

---

## 🏆 **Validación de Entregables**

### ✅ Entregable 1 - Esquema ER
- [x] Diagrama entidad-relación completo
- [x] Especificación de todas las tablas
- [x] Definición de relaciones y constraints
- [x] Documentación técnica detallada
- [x] Ubicación en `/documentation/db/`

### ✅ Entregable 2 - Diagramas de Flujo
- [x] Flujo de registro de usuario
- [x] Flujo de inicio de sesión
- [x] Flujo de creación de puesto
- [x] Flujo de búsqueda y visualización
- [x] Flujo de creación de reseña
- [x] Flujo de gestión de puestos
- [x] Ubicación en `/documentation/flowcharts/`

---

## 🏆 **Conclusión del Checkpoint 2**

El **Checkpoint 2** ha sido completado exitosamente con un diseño robusto de base de datos y flujos de usuario bien definidos. El proyecto **QUADRA** cuenta con:

- ✅ **Esquema de BD normalizado** con relaciones bien definidas
- ✅ **Diagramas de flujo completos** para todos los casos de uso
- ✅ **Documentación técnica detallada** para facilitar el desarrollo
- ✅ **Base de datos implementada** y funcionando en PostgreSQL

**Próximo paso:** Checkpoint 3 - Desarrollo de landing page, login y sign up

---

*Actualizado: 11 de agosto de 2025*
