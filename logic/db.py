import sqlite3
from datetime import datetime
from .utils import calcular_urgencia

# Ruta global de la base de datos
DB_PATH = "data/pacientes.db"

# ────────────────────────────────
# Conexión y creación de tabla
# ────────────────────────────────

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tabla():
    """Crea la tabla pacientes si no existe."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                edad INTEGER,
                gravedad INTEGER,
                sintomas TEXT,
                hospital_asignado TEXT,
                hora_llegada TEXT,
                atendido INTEGER DEFAULT 0
            );
        """)
        conn.commit()

# ────────────────────────────────
# Funciones CRUD de pacientes
# ────────────────────────────────

def insertar_paciente(nombre, edad, gravedad_base, sintomas, hospital=None):
    """Inserta paciente con cálculo de gravedad y hora actual."""
    gravedad = calcular_urgencia(gravedad_base, edad)
    llegada = datetime.now().strftime("%H:%M:%S")
    sintomas_str = ", ".join(sintomas)

    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nombre, edad, gravedad, sintomas, hospital_asignado, hora_llegada)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (nombre, edad, gravedad, sintomas_str, hospital, llegada))
        conn.commit()

def obtener_pacientes_no_atendidos():
    """Pacientes en espera, ordenados por gravedad y hora."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM pacientes
            WHERE atendido = 0
            ORDER BY gravedad DESC, hora_llegada ASC;
        """)
        pacientes = cursor.fetchall()
        return [crear_dict(cursor, row) for row in pacientes]

def obtener_pacientes_atendidos():
    """Pacientes ya atendidos (historial)."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM pacientes
            WHERE atendido = 1
            ORDER BY hora_llegada ASC;
        """)
        pacientes = cursor.fetchall()
        return [crear_dict(cursor, row) for row in pacientes]

def atender_siguiente_paciente():
    """Marca como atendido al primer paciente en espera."""
    pacientes = obtener_pacientes_no_atendidos()
    if not pacientes:
        return None
    paciente = pacientes[0]
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE pacientes SET atendido = 1 WHERE id = ?", (paciente["id"],))
        conn.commit()
    return paciente  # Se devuelve para mostrar en la vista

def marcar_paciente_atendido(id_paciente):
    """Marca un paciente como atendido (por ID)."""
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pacientes
            SET atendido = 1
            WHERE id = ?;
        """, (id_paciente,))
        conn.commit()

# ────────────────────────────────
# Utilidad para convertir filas a diccionario
# ────────────────────────────────

def crear_dict(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return dict(zip(col_names, row))
