import datetime
import json
import math

# ───────────────────────────────────────────────
# FUNCIONES GENERALES
# ───────────────────────────────────────────────

def obtener_fecha_actual():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def cargar_json(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"⚠️ Archivo no encontrado: {ruta_archivo}")
        return []
    except json.JSONDecodeError:
        print(f"⚠️ Error al decodificar el JSON: {ruta_archivo}")
        return []

def guardar_json(ruta_archivo, datos):
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)
            print(f"✅ Datos guardados en {ruta_archivo}")
    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")

# ───────────────────────────────────────────────
# FUNCIONES PARA PACIENTES
# ───────────────────────────────────────────────

def calcular_urgencia(prioridad, edad):
    if edad < 5 or edad > 65:
        return max(1, prioridad - 1)
    return prioridad

def formatear_paciente(paciente):
    return (
        f"🧑 {paciente.nombre} | Edad: {paciente.edad} | "
        f"Gravedad: {paciente.gravedad} | Síntomas: {', '.join(paciente.sintomas)}"
    )

# ───────────────────────────────────────────────
# FUNCIONES GPS – DISTANCIA ENTRE COORDENADAS
# ───────────────────────────────────────────────

def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """
    Retorna la distancia en kilómetros entre dos coordenadas usando la fórmula de Haversine.
    """
    R = 6371  # Radio de la Tierra en km
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    distancia = R * c
    return distancia
