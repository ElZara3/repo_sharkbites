# Metro CDMX - Proyecto HTML Estático

Conversión del proyecto React/Next.js a HTML puro para la plataforma de gestión del Metro de la Ciudad de México.

## 📁 Estructura de Archivos

```
proyecto/
│
├── index.html                  # Página de inicio pública
├── login.html                  # Página de inicio de sesión (solo personal)
├── public-dashboard.html       # Dashboard público (para todos)
├── formulario.html             # Formulario de reportes (sin login)
├── employee-dashboard.html     # Panel de empleados
├── manager-dashboard.html      # Panel de jefes de área
├── register.html               # Registro de personal (admin/jefes)
├── navigation.html             # Navegación interna (desarrollo)
└── README.md                   # Este archivo
```

## 🚀 Características Principales

### Jerarquía de Páginas

#### Páginas Públicas (Sin Autenticación)

1. **index.html** - Landing page
   - Hero section con información del sistema
   - Solo botón "Iniciar Sesión" para personal
   - Botón "Ver Estado del Metro" → redirige a public-dashboard.html
   - Features y características de la plataforma

2. **public-dashboard.html** - Dashboard público
   - Accesible para todos (sin login)
   - Estado general del metro
   - Alertas activas del sistema
   - Estado de todas las líneas
   - Botón "Llenar Formulario" para reportar incidentes
   - Solo botón "Iniciar Sesión" en el header (sin registro)

3. **formulario.html** - Reportar incidentes
   - Formulario público para reportar problemas
   - No requiere autenticación
   - Información de contacto opcional
   - Validación de campos en tiempo real

#### Páginas de Personal (Con Autenticación)

4. **login.html** - Autenticación de personal
   - Solo para personal del Metro
   - Redirección automática según rol
   - Credenciales de prueba disponibles

5. **employee-dashboard.html** - Panel de empleados
   - Cambio de estado (disponible/ocupado/offline)
   - Tracking GPS en tiempo real
   - Lista de incidentes asignados
   - Gestión de tareas

6. **manager-dashboard.html** - Panel de jefes de área
   - Gestión de equipo
   - Puntos críticos del sistema
   - Recomendaciones de IA para asignación
   - Tracking de disponibilidad del equipo
   - Puede registrar nuevos empleados

7. **register.html** - Registro de personal
   - Solo accesible para admins y jefes de área
   - Registro de jefes de área (por admins)
   - Registro de empleados (por jefes de área)
   - Campos dinámicos según tipo de usuario

#### Página de Desarrollo

8. **navigation.html** - Navegación interna
   - Solo para desarrollo y testing
   - Acceso rápido a todas las páginas
   - Documentación de credenciales
   - No debe usarse en producción

## 🔐 Sistema de Roles

### Jerarquía de Usuarios

```
Administrador
    ├── Puede registrar Jefes de Área
    └── Acceso completo al sistema

Jefe de Área
    ├── Puede registrar Empleados
    ├── Gestiona su equipo
    └── Asigna incidentes con IA

Empleado
    ├── Recibe incidentes asignados
    ├── Reporta su ubicación (GPS)
    └── Actualiza estado de incidentes

Público/Anónimo
    ├── Ve estado del metro
    └── Puede reportar incidentes
```

## 🛠️ Tecnologías Utilizadas

- **HTML5** - Estructura de las páginas
- **Tailwind CSS** (vía CDN) - Estilos y diseño responsivo
- **JavaScript Vanilla** - Interactividad y lógica del cliente
- **Geolocation API** - Tracking GPS para empleados
- **LocalStorage** - Almacenamiento temporal de sesión

## 📋 Uso del Proyecto

### Instalación

No requiere instalación. Simplemente abre cualquier archivo `.html` en tu navegador web.

### Para Desarrollo

1. Abre los archivos en tu editor de código favorito
2. Usa `navigation.html` para acceder rápidamente a todas las páginas
3. Usa Live Server (extensión de VS Code) para auto-reload durante desarrollo

### Simulación de Login

En `login.html`, puedes usar estos emails para simular diferentes roles:

- `admin@metro.com` → Redirige a admin-dashboard.html (no incluido aún)
- `manager@metro.com` → Redirige a manager-dashboard.html
- `employee@metro.com` → Redirige a employee-dashboard.html

La contraseña puede ser cualquiera para la simulación.

## 🔄 Funcionalidades Interactivas

### Formulario Público
- **Reportes sin login**: Cualquier persona puede reportar incidentes
- **Validación en tiempo real**: Campos se validan mientras escribes
- **Información opcional**: Contacto es opcional para reportes anónimos

### Dashboard de Empleados
- **Tracking GPS**: Usa la API de Geolocation del navegador
- **Cambio de estado**: Simulación de cambio de disponibilidad
- **Vista de incidentes**: Datos de ejemplo (mock data)

### Dashboard de Jefes de Área
- **Recomendaciones IA**: Sistema simulado de recomendaciones
- **Vista de equipo**: Tracking en tiempo real (simulado)
- **Puntos críticos**: Identificación de zonas problemáticas
- **Registro de empleados**: Puede agregar personal a su equipo

### Registro de Personal
- **Formulario dinámico**: Campos cambian según tipo de usuario
- **Validaciones**: Contraseña, email, código de empleado, etc.
- **Áreas**: Jefes se asignan a áreas específicas
- **Jerarquía**: Empleados se asignan a jefes de área

## 🔌 Integración con Backend

Para conectar con tu backend real:

1. **Reemplaza las llamadas mock** en cada archivo con llamadas fetch reales:

```javascript
// Ejemplo actual (mock):
setTimeout(() => {
    // Simulación
}, 1500);

// Cambiar a:
fetch('TU_API_URL/endpoint', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
    },
    body: JSON.stringify(datos)
})
.then(response => response.json())
.then(data => {
    // Procesar respuesta real
})
.catch(error => {
    console.error('Error:', error);
});
```

2. **Actualiza las URLs de los endpoints** en cada archivo según tu API

3. **Implementa manejo de tokens** JWT si es necesario

### Endpoints Sugeridos

```
POST /auth/login                    - Login de personal
POST /auth/register-staff           - Registro de personal (admin/jefe)
POST /reports/public                - Crear reporte público
GET  /stations/status               - Estado de estaciones
GET  /employees/my-incidents        - Incidentes del empleado
POST /employees/update-location     - Actualizar GPS
GET  /managers/team                 - Equipo del jefe
GET  /managers/recommendations/:id  - Recomendaciones IA
```

## 📱 Características Responsivas

Todos los archivos incluyen:
- Grid system responsivo de Tailwind
- Breakpoints: `sm:`, `md:`, `lg:` para diferentes tamaños
- Menús adaptables para móvil
- Cards y componentes que se ajustan automáticamente

## 🎨 Personalización

### Colores
Los colores principales están definidos en la configuración de Tailwind:
```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'metro-blue': '#0066CC'
            }
        }
    }
}
```

### Líneas del Metro
Colores oficiales incluidos en `public-dashboard.html`:
- Línea 1: #F5438E (Rosa)
- Línea 2: #0065B3 (Azul)
- Línea 3: #AF9800 (Verde Olivo)
- Y más...

## 📊 Datos de Ejemplo

Todos los archivos usan datos de ejemplo (mock data) para demostración:
- Alertas simuladas
- Estaciones del Metro CDMX
- Empleados y su estado
- Reportes e incidentes
- Recomendaciones de IA

## 🔐 Seguridad

**Nota importante**: Este es un proyecto de demostración con simulaciones.

Para producción debes:
- Implementar autenticación real con JWT
- Validar datos en el servidor
- Usar HTTPS obligatoriamente
- Sanitizar inputs del usuario
- Implementar rate limiting
- Proteger contra XSS y CSRF
- Validar roles y permisos en el backend

## 🚧 Diferencias con la Versión Original

### Cambios Principales

1. **Se eliminó dashboard.html** - Reemplazado por public-dashboard.html
2. **Nuevo formulario.html** - Reportes públicos sin autenticación
3. **register.html actualizado** - Ahora sirve para registro de personal
4. **Sin botones de registro público** - Solo personal puede autenticarse
5. **Jerarquía clara** - Admin → Jefe → Empleado → Público

### Flujos de Usuario

**Usuario Anónimo:**
```
index.html → Ver Estado → public-dashboard.html → Reportar → formulario.html
```

**Empleado:**
```
login.html → employee-dashboard.html (gestión de incidentes + GPS)
```

**Jefe de Área:**
```
login.html → manager-dashboard.html → Registrar empleado (register.html)
```

**Administrador:**
```
login.html → admin-dashboard.html → Registrar jefe (register.html)
```

## 🚧 Próximos Pasos Sugeridos

1. Crear admin-dashboard.html completo
2. Conectar con backend FastAPI real
3. Implementar WebSockets para actualizaciones en tiempo real
4. Agregar mapas interactivos con Google Maps API
5. Implementar notificaciones push
6. Agregar gráficas y analytics con Chart.js
7. Sistema de chat interno para coordinación

## 📞 Soporte

Para dudas o problemas:
1. Revisa el código JavaScript en cada archivo
2. Abre la consola del navegador (F12) para ver logs
3. Verifica que Tailwind CSS se esté cargando correctamente
4. Usa `navigation.html` para probar todas las páginas

## 📄 Licencia

Proyecto educativo para gestión del Metro CDMX.

---

**Última actualización**: Noviembre 2024
**Versión**: 2.0 (Estructura reorganizada)
