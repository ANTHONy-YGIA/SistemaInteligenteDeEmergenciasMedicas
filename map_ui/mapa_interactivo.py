# map_ui/mapa_interactivo.py

import folium
import json

# Cargar datos de hospitales
with open('./data/hospitales.json', 'r', encoding='utf-8') as f:
    hospitales = json.load(f)

# Crear un mapa centrado entre Juliaca y Puno
mapa = folium.Map(location=[-15.5, -70.1], zoom_start=9)

# Colores por nivel
colores = {
    "básico": "green",
    "intermedio": "orange",
    "crítico": "red"
}

# Agregar marcadores
for hospital in hospitales:
    lat = hospital['lat']
    lon = hospital['lon']
    nombre = hospital['nombre']
    nivel = hospital['nivel']
    direccion = hospital['direccion']
    tipo = hospital['tipo']
    telefono = hospital['telefono']

    popup_info = f"<strong>{nombre}</strong><br>Tipo: {tipo}<br>Nivel: {nivel}<br>Dirección: {direccion}<br>Tel: {telefono}"

    folium.Marker(
        location=[lat, lon],
        popup=popup_info,
        icon=folium.Icon(color=colores.get(nivel.lower(), 'blue'), icon='plus-sign')
    ).add_to(mapa)

# Guardar como HTML
mapa.save('map_ui/mapa_hospitales.html')
print("✅ Mapa generado correctamente: mapa_ui/mapa_hospitales.html")


def generar_mapa():
    mapa.save('map_ui/mapa_hospitales.html')
    print("✅ Mapa generado correctamente: map_ui/mapa_hospitales.html")