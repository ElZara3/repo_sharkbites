from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import json
import os
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)

# --- CONFIGURACIÓN DB (USA VARIABLES DE ENTORNO PARA DOCKER) ---
DB_CONFIG = {
    'dbname': os.environ.get('POSTGRES_DB', 'metro_db'),
    'user': os.environ.get('POSTGRES_USER', 'metro_user'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'metro_password'),
    'host': os.environ.get('DB_HOST', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}

# --- GESTIÓN DE ARCHIVO JSON (PARA AUTOMATIZACIONES) ---
ARCHIVO_JSON = 'automatizaciones.json'

def leer_automatizaciones():
    if not os.path.exists(ARCHIVO_JSON):
        return []
    with open(ARCHIVO_JSON, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def guardar_automatizaciones(lista):
    with open(ARCHIVO_JSON, 'w') as f:
        json.dump(lista, f, indent=4)

# --- INICIALIZACIÓN DE BASE DE DATOS (CRÍTICO PARA DOCKER) ---
def inicializar_base_datos():
    """Crea las tablas necesarias si no existen para evitar errores de arranque."""
    print("🔄 Verificando existencia de tablas...")
    
    # SQL para crear tablas si no existen (Respaldo por si falla la carga del .sql)
    commands = (
        """
        CREATE TABLE IF NOT EXISTS datos_metro_cdmx (
            id SERIAL PRIMARY KEY,
            linea VARCHAR(50),
            estacion VARCHAR(100),
            nombre_remitente VARCHAR(100),
            email_remitente VARCHAR(100),
            asunto VARCHAR(255),
            contenido TEXT,
            categoria VARCHAR(100),
            opinion VARCHAR(50),
            fecha DATE DEFAULT CURRENT_DATE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            employee_code VARCHAR(50) UNIQUE NOT NULL,
            full_name VARCHAR(100),
            status VARCHAR(20) DEFAULT 'offline',
            current_latitude DECIMAL(9,6),
            current_longitude DECIMAL(9,6),
            current_station VARCHAR(100),
            current_line VARCHAR(50),
            last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS admin_alerts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100),
            message TEXT,
            severity VARCHAR(20),
            category VARCHAR(50),
            line VARCHAR(50),
            station VARCHAR(100),
            send_to_public BOOLEAN DEFAULT FALSE,
            send_to_manager BOOLEAN DEFAULT FALSE,
            manager_category VARCHAR(50),
            created_by VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("✅ Tablas verificadas/creadas correctamente.")
    except Exception as e:
        print(f"⚠️ Advertencia verificando tablas (pueden ya existir): {e}")
    finally:
        if conn is not None:
            conn.close()

# --- SIMULADOR DE ENVÍO (SCHEDULER) ---
def revisar_y_enviar_correos():
    # print(f"[{datetime.now()}] Scheduler activo...") # Comentado para no ensuciar logs
    pass

scheduler = BackgroundScheduler()
scheduler.add_job(func=revisar_y_enviar_correos, trigger="interval", minutes=1)
scheduler.start()

# --- FILTROS SQL ---
def construir_filtros(params_request):
    linea = params_request.get('linea')
    estacion = params_request.get('estacion')
    fecha_inicio = params_request.get('fecha_inicio')
    fecha_fin = params_request.get('fecha_fin')
    categorias = params_request.getlist('categorias') 
    
    # Manejo especial para arrays en la URL (algunos frameworks los envían con [])
    if not categorias:
        categorias = params_request.getlist('categorias[]')

    where_clause = "WHERE 1=1"
    sql_params = []

    if linea and linea != "":
        where_clause += " AND linea = %s"
        sql_params.append(linea)
    if estacion and estacion != "":
        where_clause += " AND estacion = %s"
        sql_params.append(estacion)
    if fecha_inicio and fecha_fin:
        where_clause += " AND fecha BETWEEN %s AND %s"
        sql_params.append(fecha_inicio)
        sql_params.append(fecha_fin)
    if categorias:
        placeholders = ', '.join(['%s'] * len(categorias))
        where_clause += f" AND categoria IN ({placeholders})"
        sql_params.extend(categorias)

    return where_clause, sql_params

# --- ENDPOINTS ---

@app.route('/api/reporte', methods=['GET'])
def obtener_reporte():
    try:
        where_clause, params = construir_filtros(request.args)
        # MODIFICACIÓN: Seleccionamos 'contenido' explícitamente para mostrarlo en el reporte
        query = f"""
            SELECT linea, estacion, nombre_remitente, asunto, fecha, categoria, opinion
            FROM datos_metro_cdmx {where_clause}
            ORDER BY fecha DESC LIMIT 500
        """
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        
        # Mapeamos r[6] (contenido) a la clave 'opinion' como pediste
        # Esto reemplaza visualmente "Positiva/Negativa" por el texto completo del reporte
        resultados = [{
            'linea': r[0], 
            'estacion': r[1], 
            'nombre': r[2], 
            'asunto': r[3], 
            'fecha': str(r[4]), 
            'categoria': r[5], 
            'opinion': r[6], # <--- AQUÍ ESTÁ EL CAMBIO: r[6] es el CONTENIDO
        } for r in rows]
        
        cur.close(); conn.close()
        return jsonify(resultados)
    except Exception as e: 
        print(f"Error en /api/reporte: {e}")
        # Retornar lista vacía en error para no romper frontend
        return jsonify([])

@app.route('/api/dashboard', methods=['GET'])
def obtener_estadisticas():
    try:
        where_clause, params = construir_filtros(request.args)
        linea_filtro = request.args.get('linea')
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 1. Total
        cur.execute(f"SELECT COUNT(*) FROM datos_metro_cdmx {where_clause}", tuple(params))
        total = cur.fetchone()[0]

        # 2. Gráfico Principal (Top Estaciones o Líneas)
        if linea_filtro:
            query_top = f"SELECT estacion, COUNT(*) as total FROM datos_metro_cdmx {where_clause} GROUP BY estacion ORDER BY total DESC LIMIT 5"
            titulo = f"Top Estaciones ({linea_filtro})"
        else:
            query_top = f"SELECT linea, COUNT(*) as total FROM datos_metro_cdmx {where_clause} GROUP BY linea ORDER BY total DESC LIMIT 5"
            titulo = "Top Líneas (Global)"
            
        cur.execute(query_top, tuple(params))
        top_data = cur.fetchall()

        # 3. Por Opinión (Aquí sí usamos la columna opinion para el gráfico de pastel)
        cur.execute(f"SELECT opinion, COUNT(*) FROM datos_metro_cdmx {where_clause} GROUP BY opinion", tuple(params))
        opiniones = cur.fetchall()
        
        cur.close(); conn.close()
        
        return jsonify({
            'total': total, 
            'titulo_grafico': titulo,
            'grafico_principal': {'labels': [r[0] for r in top_data], 'data': [r[1] for r in top_data]},
            'por_opinion': {'labels': [r[0] for r in opiniones], 'data': [r[1] for r in opiniones]}
        })
    except Exception as e: 
        print(f"Error en /api/dashboard: {e}")
        return jsonify({'error': str(e)}), 500

# --- ENDPOINTS DE AUTOMATIZACIÓN ---
@app.route('/api/automatizacion', methods=['GET', 'POST'])
def gestionar_automatizacion():
    if request.method == 'POST':
        data = request.json
        tareas = leer_automatizaciones()
        nuevo_id = int(datetime.now().timestamp())
        nueva_tarea = {
            'id': nuevo_id,
            'email': data.get('email'),
            'fecha_inicio': data.get('fecha_inicio'),
            'frecuencia': data.get('frecuencia'),
            'filtros': data.get('filtros')
        }
        tareas.append(nueva_tarea)
        guardar_automatizaciones(tareas)
        return jsonify({'mensaje': 'Guardado', 'id': nuevo_id})
    else:
        tareas = leer_automatizaciones()
        tareas.sort(key=lambda x: x['id'], reverse=True)
        return jsonify(tareas)

@app.route('/api/automatizacion/<int:id>', methods=['DELETE'])
def borrar_automatizacion(id):
    tareas = leer_automatizaciones()
    tareas_filtradas = [t for t in tareas if t['id'] != id]
    if len(tareas) == len(tareas_filtradas):
        return jsonify({'error': 'No encontrado'}), 404
    guardar_automatizaciones(tareas_filtradas)
    return jsonify({'mensaje': 'Eliminado'})

# --- TIEMPO REAL / EMPLEADOS ---
@app.route('/api/employee/update-location', methods=['POST'])
def actualizar_ubicacion_empleado():
    try:
        data = request.json
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            UPDATE employees 
            SET current_latitude = %s, current_longitude = %s, current_station = %s, current_line = %s, last_update = NOW()
            WHERE employee_code = %s RETURNING id
        """, (data.get('latitude'), data.get('longitude'), data.get('station'), data.get('line'), data.get('employee_code')))
        result = cur.fetchone()
        conn.commit(); cur.close(); conn.close()
        return jsonify({'success': True} if result else {'error': 'Empleado no encontrado'}), 200 if result else 404
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/api/admin/create-alert', methods=['POST'])
def crear_alerta():
    try:
        d = request.json
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO admin_alerts (title, message, severity, category, line, station, send_to_public, send_to_manager, manager_category, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (d.get('title'), d.get('message'), d.get('severity'), d.get('category'), d.get('line'), d.get('station'), d.get('send_to_public'), d.get('send_to_manager'), d.get('category'), d.get('created_by', 'Admin')))
        conn.commit(); cur.close(); conn.close()
        return jsonify({'success': True})
    except Exception as e: return jsonify({'error': str(e)}), 500

@app.route('/api/public/alerts', methods=['GET'])
def obtener_alertas_publicas():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id, title, message, severity, line, station, created_at FROM admin_alerts WHERE send_to_public = true ORDER BY created_at DESC LIMIT 20")
        rows = cur.fetchall()
        cur.close(); conn.close()
        return jsonify([{'id':r[0],'title':r[1],'message':r[2],'severity':r[3],'line':r[4],'station':r[5],'created_at':str(r[6])} for r in rows])
    except Exception as e: return jsonify({'error': str(e)}), 500

# --- HEALTH CHECK & MAIN ---
@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, 'w') as f: json.dump([], f)
    
    print("⏳ Esperando base de datos...")
    max_retries = 30
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("✅ Conexión a PostgreSQL exitosa.")
            
            # --- CRÍTICO: INICIALIZAR TABLAS ---
            inicializar_base_datos()
            # -----------------------------------
            
            break
        except Exception as e:
            if i == max_retries - 1:
                print("❌ Error fatal: No se pudo conectar a la BD.")
                exit(1)
            time.sleep(2)
    
    app.run(debug=True, host='0.0.0.0', port=5000)