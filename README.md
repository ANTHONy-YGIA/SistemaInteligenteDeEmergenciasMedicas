# SOS Juliaca – Mapa Inteligente de Emergencias Médicas

Este proyecto es un sistema de triaje médico que permite registrar pacientes, asignarles un nivel de prioridad, y mostrar en un mapa interactivo los hospitales más cercanos disponibles en la ciudad de Juliaca, Perú.

## Descripción del sistema

El sistema está diseñado para ayudar en situaciones de emergencia, simulando el proceso de triaje hospitalario. Los pacientes son clasificados en cinco niveles de gravedad: leve, moderado, grave, muy grave y crítico. Dependiendo del nivel, se asigna un hospital disponible en el mapa.

El proyecto cuenta con:

- Registro de pacientes
- Simulación del triaje
- Visualización de hospitales en un mapa interactivo

## Requisitos del sistema

Este proyecto necesita los siguientes componentes instalados:

- Python 3.10 o superior
- Flask (para el servidor web)
- Folium (para generar mapas)
- Un navegador web (para visualizar el sistema)

## Estructura del proyecto
SOS-Juliaca/
│
├── app.py # Archivo principal
├── logic/
│ ├── simulador.py
│ ├── triaje.py
│ └── utils.py
| └── db.py
├── map_ui/
│ └── mapa.py
├── data/
│ └── hospitales.json
| └── pacientes.db
├── templates/
│ └── index.html # Interfaz del sistema
| └── atender.html # Interfaz de la atencion
| └── mapa.html # Interfaz del mapa
| └── pacientes.html # Interfaz para ver los pacientes
| └── registrar.html # Interfaz del registro
| └── ruta.html # Interfaz del sistema deruta
| └── simulador.html # Interfaz del sistema de simulacion
├── static/
│ ├── style.css # Estilos
│ └── script.js # Lógica de la interfaz (vacío por ahora)
├── assets/ # Carpeta para imágenes o íconos
└── README.md # Este archivo

## Observaciones

- El mapa muestra la ubicación de los hospitales registrados.
- La lógica de asignación médica se basa en la gravedad del paciente.
- El diseño puede ampliarse con más estilos, validaciones o mejoras visuales.

---