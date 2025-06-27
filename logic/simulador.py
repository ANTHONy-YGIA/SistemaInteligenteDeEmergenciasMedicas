#from .triaje import Triaje

#def generar_pacientes():
#    triaje = Triaje()

#    triaje.agregar_paciente("Juan Pérez", 2, ["fiebre", "tos"], "Hospital Carlos Monge", edad=70)
#    triaje.agregar_paciente("Ana Torres", 1, ["dificultad para respirar"], "Hospital Regional", edad=25)
#    triaje.agregar_paciente("Luis Quispe", 4, ["dolor de cabeza"], edad=10)
#    triaje.agregar_paciente("Rosa Mamani", 3, ["dolor abdominal"], "Clínica Americana", edad=33)

#    return triaje

# logic/simulador.py

from .triaje import Triaje
from .utils import cargar_json

# Crear instancia del sistema de triaje
triaje = Triaje()

# Cargar pacientes desde archivo JSON
pacientes = cargar_json("data/pacientes.json")

# Agregarlos al sistema
for p in pacientes:
    triaje.agregar_paciente(
        nombre=p["nombre"],
        gravedad=p["gravedad"],
        sintomas=p["sintomas"],
        hospital_asignado=p.get("hospital_asignado"),
        edad=p.get("edad", 30)
    )

# Mostrar pacientes en espera
print("📋 Pacientes en espera:")
for paciente in triaje.mostrar_en_espera():
    print("-", paciente)

# Simular atención
print("\n🏥 Atención médica:")
while True:
    resultado = triaje.atender_paciente()
    print(resultado)
    if resultado == "No hay pacientes en espera.":
        break

