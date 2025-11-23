from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --- 1. BASE DE DATOS Y FECHA ---
import os
import psycopg2
from datetime import date # Para obtener la fecha actual

# **IMPORTANTE:** Usa esta configuración para conectar a tu base de datos.
# Asegúrate de que las variables de entorno estén configuradas en tu entorno de ejecución
DB_CONFIG = {
    'dbname': os.environ.get('POSTGRES_DB', 'metro_db'),
    'user': os.environ.get('POSTGRES_USER', 'metro_user'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'metro_password'),
    'host': os.environ.get('DB_HOST', 'postgres'),
    'port': os.environ.get('DB_PORT', '5432')
}

def insertar_reporte_db(datos_reporte: dict):
    """
    Establece conexión a PostgreSQL e inserta el registro del reporte.
    """
    conn = None
    try:
        # Intenta conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # SQL con placeholders (%s) para prevenir inyecciones SQL (SQL Injection)
        # Asegúrate de que la tabla 'datos_metro_cdmx' y sus columnas existan
        sql_insert = """
        INSERT INTO datos_metro_cdmx (
            linea, estacion, nombre_remitente, email_remitente, asunto, 
            contenido, categoria, opinion, fecha
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        
        # El orden de los valores debe coincidir con el orden de las columnas en el SQL
        values = (
            datos_reporte['linea'],
            datos_reporte['estacion'],
            datos_reporte['nombre_remitente'],
            datos_reporte['email_remitente'],
            datos_reporte['asunto'],
            datos_reporte['contenido'],
            datos_reporte['categoria'],
            datos_reporte['opinion'], # Este es el campo predicho por el modelo
            datos_reporte['fecha']
        )
        
        # Ejecutar la inserción
        cur.execute(sql_insert, values)
        
        # Confirmar la transacción
        conn.commit()
        cur.close()
        print("-> Registro insertado exitosamente en PostgreSQL.")
        
    except psycopg2.Error as e:
        # En caso de error, hacer un rollback y lanzar una excepción HTTP
        print(f"ERROR de PostgreSQL: {e}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar en la base de datos: {e}")
        
    finally:
        # Asegurarse de cerrar la conexión
        if conn:
            conn.close()

# --- 2. CONFIGURACIÓN DEL MODELO ML (Tu código) ---
model_path = "./final_model"
print(f"Cargando modelo desde {model_path}...")

try:
    # Cargamos el modelo una sola vez al iniciar el servidor
    # (Asumimos que el modelo y el tokenizador están disponibles)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()
    print("Modelo cargado exitosamente.")
except Exception as e:
    print(f"ERROR: No se pudo cargar el modelo. Detalle del error: {e}")
    # Si el modelo falla al cargar, las predicciones fallarán
    # Se recomienda que el usuario compruebe la ruta y archivos.

def predecir_sentimiento(texto):
    """
    Realiza la predicción de sentimiento (etiqueta/opinión) para un texto dado.
    """
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    probs = F.softmax(outputs.logits, dim=-1)
    pred_idx = torch.argmax(probs).item()
    
    etiqueta = model.config.id2label.get(pred_idx, str(pred_idx))
    confianza = probs[0][pred_idx].item() 
    return etiqueta, confianza

# --- 3. CONFIGURACIÓN DE FASTAPI ---
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. MODELO DE DATOS (Esquema del JSON) ---
class ReporteMetro(BaseModel):
    linea: str
    estacion: str
    nombre_remitente: Optional[str] = None
    email_remitente: Optional[str] = None
    categoria: str
    asunto: str
    contenido: str

# --- 5. ENDPOINT (Ruta de la API) ---
@app.post("/reportes")
async def recibir_reporte(reporte: ReporteMetro):
    print("\n--- Nuevo Reporte Recibido ---")
    
    # 1. Usar el asunto para la predicción de sentimiento
    texto_a_analizar = reporte.asunto
    
    # 2. Realizar predicción
    try:
        etiqueta_opinion, confianza = predecir_sentimiento(texto_a_analizar)
        
        # 3. Preparar los datos para la base de datos
        datos_para_db = reporte.model_dump()
        datos_para_db['opinion'] = etiqueta_opinion
        # Usar la fecha actual del sistema para la columna 'fecha'
        datos_para_db['fecha'] = date.today().strftime('%Y-%m-%d')
        
        print(f"Asunto: '{texto_a_analizar}'")
        print(f"Categoría Usuario: {reporte.categoria}")
        print(f"Predicción del Modelo (Opinión): {etiqueta_opinion} (Confianza: {confianza:.4f})")

        # 4. Insertar el reporte en la base de datos
        insertar_reporte_db(datos_para_db)
        
        # 5. Respuesta al cliente (Frontend)
        return {
            "mensaje": "Reporte recibido, procesado y guardado en DB",
            "analisis_ia": {
                "sentimiento": etiqueta_opinion,
                "confianza": round(confianza, 4)
            }
        }
        
    except HTTPException as e:
        # Re-lanzar las excepciones HTTP generadas por la función de DB
        raise e
    except Exception as e:
        print(f"Error al procesar modelo o DB: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor al procesar el reporte.")

# Para correr el servidor:
# uvicorn app:app --reload