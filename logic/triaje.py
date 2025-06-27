import heapq
from datetime import datetime
from . import db
from .utils import calcular_urgencia

class Paciente:
    def __init__(self, id, nombre, edad, gravedad, sintomas, llegada, hospital_asignado=None):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.gravedad = gravedad
        self.sintomas = sintomas
        self.hora_llegada = llegada
        self.hospital_asignado = hospital_asignado

    def __lt__(self, other):
        return self.gravedad < other.gravedad

    def __repr__(self):
        return (
            f"{self.nombre} | Edad: {self.edad} | Gravedad: {self.gravedad} | "
            f"Síntomas: {self.sintomas} | "
            f"Llegada: {self.hora_llegada} | "
            f"Hospital: {self.hospital_asignado or 'No asignado'}"
        )

class Triaje:
    def __init__(self):
        db.crear_tabla()

    def agregar_paciente(self, nombre, gravedad, sintomas, hospital_asignado=None, edad=30):
        gravedad_real = calcular_urgencia(gravedad, edad)
        llegada = datetime.now().strftime("%H:%M:%S")
        db.insertar_paciente(nombre, edad, gravedad_real, sintomas, hospital_asignado, llegada)

    def mostrar_en_espera(self):
        pacientes_raw = db.obtener_pacientes_en_espera()
        cola_prioridad = []
        for p in pacientes_raw:
            paciente = Paciente(p[0], p[1], p[2], p[3], p[4], p[6], p[5])
            heapq.heappush(cola_prioridad, paciente)
        return [str(p) for p in cola_prioridad]

    def atender_paciente(self):
        pacientes_raw = db.obtener_pacientes_en_espera()
        if not pacientes_raw:
            return "No hay pacientes en espera."

        # Obtener paciente con menor gravedad
        paciente = sorted(pacientes_raw, key=lambda p: p[3])[0]
        db.marcar_paciente_atendido(paciente[0])

        return f"✅ Atendiendo a: {paciente[1]} | Edad: {p[2]} | Gravedad: {p[3]} | Síntomas: {p[4]} | Hospital: {p[5] or 'No asignado'}"

