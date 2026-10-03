"""
FastRoutes - Backend (Flask)

POST /api/ruta
    1. Descarga el grafo dirigido de la zona (grafo.py)
    2. Ejecuta Dijkstra desde el almacén y cada entrega (algoritmos.py)
    3. Ordena las visitas para minimizar el tiempo del circuito cerrado
    4. Devuelve el trazo, el orden de visita y los tiempos
"""
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

import algoritmos
import grafo

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(__name__, static_folder=None)

# --- Reglas de negocio ---
MAX_PARADAS = 15
TIEMPO_SERVICIO_MIN = 5
MARGEN_GRADOS = 0.01          # ~1.1 km alrededor de los puntos
EXTENSION_MAX_GRADOS = 0.35   # evita descargar mapas gigantes

# (latitud, longitud, radio en km): una ruta no puede salir de su ciudad
CIUDADES = {
    "Lima": (-12.0464, -77.0428, 40),
    "Arequipa": (-16.4090, -71.5375, 20),
    "Cusco": (-13.5320, -71.9675, 15),
    "Trujillo": (-8.1091, -79.0215, 20),
    "Piura": (-5.1945, -80.6328, 20),
}


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/<path:archivo>")
def estaticos(archivo):
    return send_from_directory(FRONTEND_DIR, archivo)


@app.get("/api/health")
def health():
    return jsonify(estado="ok")


@app.post("/api/ruta")
def calcular_ruta():
    datos = request.get_json(silent=True) or {}
    puntos = datos.get("puntos", [])
    ciudad = datos.get("ciudad")

    # ---- Validaciones (reglas de negocio) ----
    if len(puntos) < 2:
        return jsonify(error="Selecciona el almacén y al menos 1 entrega."), 400
    paradas = len(puntos) - 1
    if paradas > MAX_PARADAS:
        return jsonify(error=f"Máximo {MAX_PARADAS} paradas por viaje."), 400

    if ciudad in CIUDADES:
        lat_c, lng_c, radio = CIUDADES[ciudad]
        for lng, lat in puntos:
            if grafo.distancia_km(lat_c, lng_c, lat, lng) > radio:
                return jsonify(error=f"Todos los puntos deben estar dentro de {ciudad}."), 400

    lngs = [p[0] for p in puntos]
    lats = [p[1] for p in puntos]
    if max(lngs) - min(lngs) > EXTENSION_MAX_GRADOS or max(lats) - min(lats) > EXTENSION_MAX_GRADOS:
        return jsonify(error="Los puntos están demasiado separados."), 400

    # ---- 1. Grafo dirigido de la zona ----
    try:
        adj, coords = grafo.obtener_grafo(
            max(lats) + MARGEN_GRADOS, min(lats) - MARGEN_GRADOS,
            max(lngs) + MARGEN_GRADOS, min(lngs) - MARGEN_GRADOS,
        )
    except Exception as e:
        app.logger.exception("Error al cargar el grafo")
        return jsonify(error="No se pudo descargar el mapa de calles. Revisa tu conexión."), 502

    nodos = [grafo.nodo_mas_cercano(coords, lng, lat) for lng, lat in puntos]

    # ---- 2. Dijkstra desde cada punto ----
    resultados = []
    for nodo in nodos:
        objetivos = set(nodos) - {nodo}
        resultados.append(algoritmos.dijkstra(adj, nodo, objetivos))

    n = len(nodos)
    costos = [[0.0 if i == j else resultados[i][0].get(nodos[j], algoritmos.INF)
               for j in range(n)] for i in range(n)]
    if any(costos[i][j] == algoritmos.INF for i in range(n) for j in range(n) if i != j):
        return jsonify(error="Algún punto es inalcanzable por las calles. Mueve los puntos."), 422

    # ---- 3. Orden óptimo de visitas ----
    orden, metodo = algoritmos.mejor_circuito(costos)

    # ---- 4. Armar el trazo completo y los totales ----
    secuencia = [0] + orden + [0]
    linea = []
    metros_total = 0.0
    segundos_total = 0.0
    for a, b in zip(secuencia, secuencia[1:]):
        _, metros, previo = resultados[a]
        segundos_total += costos[a][b]
        if nodos[a] != nodos[b]:
            metros_total += metros[nodos[b]]
            for geom in algoritmos.reconstruir_camino(previo, nodos[a], nodos[b]):
                for punto in geom:
                    if not linea or linea[-1] != list(punto):
                        linea.append([punto[0], punto[1]])

    mov_min = segundos_total / 60
    servicio_min = paradas * TIEMPO_SERVICIO_MIN

    return jsonify(
        geometry={"type": "LineString", "coordinates": linea},
        orden=orden,
        metodo=metodo,
        distancia_m=round(metros_total, 1),
        duracion_movimiento_min=round(mov_min, 1),
        tiempo_servicio_min=servicio_min,
        tiempo_total_min=round(mov_min + servicio_min, 1),
        paradas=paradas,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
