"""FastRoutes - Constantes y reglas de negocio."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

MAX_PARADAS = 15
TIEMPO_SERVICIO_MIN = 5
MARGEN_GRADOS = 0.01          # ~1.1 km alrededor de los puntos
EXTENSION_MAX_GRADOS = 0.35   # evita descargar mapas gigantes
PRECARGA_GRADOS = 0.05        # ~5.5 km alrededor del almacén (precarga en segundo plano)
LIMITE_EXACTO = 12            # hasta aquí se usa Held-Karp; después, heurística

# (latitud, longitud, radio en km): una ruta no puede salir de su ciudad
CIUDADES = {
    "Lima": (-12.0464, -77.0428, 40),
    "Arequipa": (-16.4090, -71.5375, 20),
    "Cusco": (-13.5320, -71.9675, 15),
    "Trujillo": (-8.1091, -79.0215, 20),
    "Piura": (-5.1945, -80.6328, 20),
}
