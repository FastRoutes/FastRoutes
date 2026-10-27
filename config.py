"""FastRoutes - Constantes y reglas de negocio."""
import json
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
# Fuente única de ciudades: la comparte el front (frontend/ciudades.json)
with open(FRONTEND_DIR / "ciudades.json", encoding="utf-8") as f:
    CIUDADES = {c["nombre"]: (c["lat"], c["lng"], c["radio_km"]) for c in json.load(f)}
