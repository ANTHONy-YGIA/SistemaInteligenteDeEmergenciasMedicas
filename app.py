from flask import Flask, render_template, request, redirect, url_for, session
from map_ui.mapa_interactivo import generar_mapa
from logic.db import (
    crear_tabla,
    insertar_paciente,
    obtener_pacientes_no_atendidos,
    obtener_pacientes_atendidos,
    atender_siguiente_paciente
)
from logic.utils import cargar_json, calcular_distancia_km
import os, shutil

app = Flask(__name__)
app.secret_key = "sos_juliaca_key"  # necesario para usar session

# ─────────────────────────────────────────
# 1. Crear tabla e importar hospitales
# ─────────────────────────────────────────
crear_tabla()
HOSPITALES = cargar_json(os.path.join("data", "hospitales.json"))

# ─────────────────────────────────────────
# 2. Rutas principales
# ─────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        edad = int(request.form["edad"])
        gravedad = int(request.form["gravedad"])
        sintomas = [s.strip() for s in request.form["sintomas"].split(",")]

        lat = request.form.get("lat")
        lon = request.form.get("lon")
        hospital = request.form.get("hospital") or None

        # Asignar hospital automáticamente si no se ingresó manualmente
        if not hospital and lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                hospital = asignar_hospital_mas_cercano(lat, lon)
            except:
                hospital = None

        # Guardar en la base de datos
        insertar_paciente(nombre, edad, gravedad, sintomas, hospital)

        # Guardar en sesión para redireccionar
        session["lat"] = lat
        session["lon"] = lon
        session["hospital"] = hospital
        return redirect(url_for("ruta_hospital"))

    return render_template("registrar.html")

def asignar_hospital_mas_cercano(lat, lon):
    min_dist = float("inf")
    hospital_cercano = None
    for h in HOSPITALES:
        dist = calcular_distancia_km(lat, lon, h["lat"], h["lon"])
        if dist < min_dist:
            min_dist = dist
            hospital_cercano = h["nombre"]
    return hospital_cercano

@app.route("/ruta")
def ruta_hospital():
    lat = session.get("lat")
    lon = session.get("lon")
    hospital_nombre = session.get("hospital")

    if not lat or not lon or not hospital_nombre:
        return "Información de ubicación incompleta.", 400

    hospital = next((h for h in HOSPITALES if h["nombre"] == hospital_nombre), None)

    if not hospital:
        return "Hospital no encontrado.", 404

    url_maps = f"https://www.google.com/maps/dir/{lat},{lon}/{hospital['lat']},{hospital['lon']}"

    return render_template("ruta.html", hospital=hospital, url_maps=url_maps)

@app.route("/pacientes")
def ver_pacientes():
    pacientes = obtener_pacientes_no_atendidos()
    return render_template("pacientes.html", pacientes=pacientes)

@app.route("/atender")
def atender():
    paciente = atender_siguiente_paciente()
    if paciente:
        mensaje = f"✅ Atendiendo a: {paciente['nombre']} - Gravedad: {paciente['gravedad']}"
    else:
        mensaje = "No hay pacientes en espera."
    return render_template("atender.html", resultado=mensaje)

@app.route("/mapa")
def mapa():
    generar_mapa()
    origen = os.path.join("map_ui", "mapa_hospitales.html")
    destino = os.path.join("static", "mapa_hospitales.html")
    shutil.copy(origen, destino)
    return render_template("mapa.html")

# ─────────────────────────────────────────
# 3. Simulador (modo doctor)
# ─────────────────────────────────────────

@app.route("/simulador")
def simulador():
    pacientes_espera = obtener_pacientes_no_atendidos()
    pacientes_atendidos = obtener_pacientes_atendidos()
    return render_template("simulador.html",
                           pacientes_espera=pacientes_espera,
                           pacientes_atendidos=pacientes_atendidos)

@app.route("/simulador/atender", methods=["POST"])
def atender_simulador():
    atender_siguiente_paciente()
    return redirect(url_for("simulador"))

# ─────────────────────────────────────────
# 4. Iniciar servidor Flask
# ─────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)