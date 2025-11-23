# 🚇 Sistema de Reportes Metro CDMX - Versión Windows

## ✅ Versión Simplificada para Windows

Esta es una versión **minimalista y optimizada** que incluye:
- ✅ PostgreSQL con 7,500 registros del metro
- ✅ Sistema de Reportes Flask (puerto 5000)
- ✅ Sin dependencias complejas
- ✅ Funciona perfectamente en Windows

---

## 📋 Requisitos Previos

Solo necesitas:
1. **Docker Desktop para Windows** 
   - Descarga: https://www.docker.com/products/docker-desktop/
   - Instala y asegúrate de que esté corriendo (ícono de Docker en la bandeja)

---

## 🚀 Instalación (3 pasos)

### 1️⃣ Extraer el proyecto

Extrae el ZIP en cualquier carpeta, por ejemplo:
```
C:\Users\TuUsuario\metro-reportes-simple\
```

### 2️⃣ Abrir PowerShell o CMD

Click derecho en la carpeta del proyecto → **"Abrir en Terminal"**

O manualmente:
```powershell
cd C:\Users\TuUsuario\metro-reportes-simple
```

### 3️⃣ Iniciar el sistema

```powershell
docker-compose up --build
```

**⏱️ Primera vez**: 5-10 minutos (descarga imágenes y carga 7,500 registros)  
**Siguientes veces**: 30 segundos

---

## ✅ Verificar que funciona

Espera a ver este mensaje en la consola:

```
metro_reportes    | ✅ Conexión exitosa con PostgreSQL!
metro_reportes    | * Running on http://0.0.0.0:5000
```

Luego abre tu navegador en:

## 🌐 http://localhost:5000

¡Listo! Deberías ver la interfaz de reportes.

---

## 🎯 Cómo Usar el Sistema

### 1. Generar un reporte

1. Selecciona una **Línea** (Línea 1, 2, 3, etc.)
2. (Opcional) Selecciona una **Estación**
3. (Opcional) Marca **Categorías** (Retrasos, Limpieza, etc.)
4. (Opcional) Selecciona **Rango de fechas**
5. Click en **"Buscar"**

Verás:
- 📊 Gráfico de barras
- 📈 Gráfico circular de opiniones
- 📋 Tabla con todos los registros

### 2. Exportar a PDF

1. Genera un reporte
2. Click en **"Generar PDF"**
3. Se descarga automáticamente

### 3. Automatizar reportes

1. Click en **"Automatizar"**
2. Ingresa email, fecha y frecuencia
3. Guarda

---

## 🛠️ Comandos Útiles

### Detener el sistema
```powershell
docker-compose down
```

### Ver logs en tiempo real
```powershell
docker-compose logs -f
```

### Reiniciar
```powershell
docker-compose restart
```

### Borrar todo y empezar de cero
```powershell
docker-compose down -v
docker-compose up --build
```

---

## 🔍 Solución de Problemas

### ❌ Error: "Puerto 5000 ya en uso"

**Opción 1**: Cerrar el programa que usa el puerto 5000
```powershell
netstat -ano | findstr :5000
taskkill /PID <numero> /F
```

**Opción 2**: Cambiar el puerto

Edita `docker-compose.yml` línea 23:
```yaml
ports:
  - "5001:5000"  # Cambia 5001 por el que quieras
```

Luego usa: http://localhost:5001

---

### ❌ Docker no responde

1. Abre Docker Desktop
2. Click en el ícono de Docker en la bandeja
3. Verifica que diga "Docker Desktop is running"
4. Si no, reinicia Docker Desktop

---

### ❌ "Timeout" al descargar paquetes

Si ves errores de timeout al hacer `docker-compose up --build`:

1. Verifica tu conexión a Internet
2. Espera unos minutos y reintenta:
```powershell
docker-compose down
docker-compose up --build
```

3. Si persiste, edita `reportes/Dockerfile` línea 14:
```dockerfile
RUN pip install --timeout=300 --retries=10 --no-cache-dir -r requirements.txt
```

---

### ❌ La base de datos está vacía

```powershell
# Recrear todo
docker-compose down -v
docker-compose up --build
```

Esto recarga los 7,500 registros.

---

## 📊 Datos Incluidos

### Base de Datos: `datos_metro_cdmx`

**7,500 registros** con:

**Líneas**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, A, B

**Categorías**:
1. Trabajadores
2. Consultas/Dudas
3. Sugerencias
4. Retrasos
5. Asientos reservados
6. Fallas Técnicas
7. Mantenimiento/Limpieza
8. Accesibilidad
9. Cancelaciones
10. Información/Comunicación
11. Seguridad
12. Trato del Personal

**Opiniones**: Positiva, Negativa, Neutra

**Fechas**: 2023-01-01 a 2025-11-23

---

## 📁 Estructura del Proyecto

```
metro-reportes-simple/
├── docker-compose.yml      # Configuración de servicios
├── sql/
│   └── base_de_datos_metro.sql  # 7,500 registros
└── reportes/
    ├── app.py              # Backend Flask
    ├── index.html          # Interfaz web
    ├── Dockerfile
    └── requirements.txt
```

---

## 🎓 API Endpoints

Además de la interfaz web, puedes usar la API:

### Obtener estadísticas
```
http://localhost:5000/api/dashboard
```

### Obtener reportes
```
http://localhost:5000/api/reporte
```

### Filtrar por línea
```
http://localhost:5000/api/reporte?linea=Línea 1
```

### Health check
```
http://localhost:5000/health
```

---

## 🔗 Conectar desde otras aplicaciones

Si quieres conectarte a PostgreSQL desde otras apps:

**Host**: `localhost`  
**Puerto**: `5432`  
**Usuario**: `metro_user`  
**Contraseña**: `metro_password`  
**Base de datos**: `metro_db`  
**Tabla principal**: `datos_metro_cdmx`

Puedes usar:
- DBeaver
- pgAdmin
- TablePlus
- Cualquier cliente PostgreSQL

---

## ⚙️ Personalización

### Cambiar credenciales de la BD

Edita `docker-compose.yml` líneas 6-8:
```yaml
environment:
  POSTGRES_USER: tu_usuario
  POSTGRES_PASSWORD: tu_password
  POSTGRES_DB: tu_database
```

### Agregar más categorías

Edita `reportes/index.html` líneas 88-100

### Cambiar puerto del servicio

Edita `docker-compose.yml` línea 23:
```yaml
ports:
  - "8080:5000"  # Usar puerto 8080 en tu máquina
```

---

## 📞 Soporte

Si tienes problemas:

1. Verifica que Docker Desktop esté corriendo
2. Revisa los logs: `docker-compose logs -f`
3. Reinicia: `docker-compose restart`
4. Borra y recrea: `docker-compose down -v` y `docker-compose up --build`

---

## ✨ Ventajas de esta versión

✅ **Simple**: Solo 2 servicios (PostgreSQL + Reportes)  
✅ **Rápido**: Inicia en 30 segundos  
✅ **Ligero**: ~150 MB de imágenes Docker  
✅ **Compatible**: Funciona en Windows 10/11  
✅ **Completo**: 7,500 registros reales del metro  
✅ **Sin configuración**: Todo funciona con valores por defecto  

---

## 🎉 ¡Listo!

Ejecuta:
```powershell
docker-compose up --build
```

Y abre: **http://localhost:5000**

¡Disfruta tu sistema de reportes! 🚇📊
