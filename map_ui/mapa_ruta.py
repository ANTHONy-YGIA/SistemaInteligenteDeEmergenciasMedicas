# map_ui/mapa_ruta.py
import folium
from logic.utils import cargar_json

def generar_mapa_ruta(lat_user, lon_user, hospital_asignado):
    hospitales = cargar_json("data/hospitales.json")

    # Encontrar hospital seleccionado
    hospital = next((h for h in hospitales if h["nombre"] == hospital_asignado), None)
    if not hospital:
        print("❌ Hospital no encontrado")
        return

    # Crear mapa centrado entre paciente y hospital
    lat_centro = (lat_user + hospital["lat"]) / 2
    lon_centro = (lon_user + hospital["lon"]) / 2
    m = folium.Map(location=[lat_centro, lon_centro], zoom_start=14)

    # Marcador del paciente
    folium.Marker(
        [lat_user, lon_user],
        tooltip="📍 Tu ubicación",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Marcador del hospital
    folium.Marker(
        [hospital["lat"], hospital["lon"]],
        tooltip=f"🏥 {hospital['nombre']}",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Línea entre paciente y hospital
    folium.PolyLine(
        [(lat_user, lon_user), (hospital["lat"], hospital["lon"])],
        color="green", weight=4, opacity=0.6
    ).add_to(m)

    m.save("static/mapa_ruta.html")
    print("✅ Mapa de ruta generado: static/mapa_ruta.html")
