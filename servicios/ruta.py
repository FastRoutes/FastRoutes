"""Cálculo de la ruta de un viaje (almacén -> entregas -> almacén).

Flujo:
    1. Los puntos (negocio y entregas) se ajustan a nodos del mapa de calles.
    2. Dijkstra halla los caminos mínimos entre todos esos nodos.
    3. Con esos caminos como aristas se arma el grafo artificial donde se resuelve el TSP.
    4. Greedy (aproximación) obtiene rápido una solución inicial.
    5. Or-opt mejora el tour (válido para TSP asimétrico).
    6. El tour se traslada al mapa real cambiando cada arista por su camino de calles.
"""
import logging
import time

import algoritmos
import grafo
from algoritmos import GrafoArtificial, PuntoInalcanzable
from config import DISTANCIA_MAX_A_CALLE_M, OR_OPT_SEGMENTO_MAX, TIEMPO_SERVICIO_MIN

from .errores import ErrorNegocio
from .validaciones import caja_con_margen, validar_solicitud

log = logging.getLogger(__name__)


def _cargar_grafo(puntos):
    """Mapa de calles (grafo dirigido) que cubre todos los puntos."""
    try:
        return grafo.obtener_grafo(*caja_con_margen(puntos))
    except Exception:
        log.exception("Error al cargar el grafo")
        raise ErrorNegocio(
            "No se pudo obtener el mapa de calles de esa zona. "
            "Inténtalo de nuevo o acerca los puntos a zonas con calles.", 502)


def _ajustar_a_calles(g, puntos):
    """Paso 1: nodo de calle más cercano a cada punto seleccionado."""
    nodos = []
    for i, (lng, lat) in enumerate(puntos):
        nodo, metros = g.nodo_y_distancia(lng, lat)
        if metros > DISTANCIA_MAX_A_CALLE_M:
            quien = "El negocio" if i == 0 else f"La entrega #{i}"
            raise ErrorNegocio(f"{quien} está a {metros:.0f} m de la calle más cercana. Muévelo.", 422)
        nodos.append(nodo)
    return nodos


def _grafo_artificial(g, nodos):
    """Pasos 2 y 3: Dijkstra entre los nodos y grafo artificial con esos caminos como aristas."""
    try:
        return GrafoArtificial.desde_calles(g.adj, nodos)
    except PuntoInalcanzable:
        raise ErrorNegocio("Algún punto es inalcanzable por las calles. Mueve los puntos.", 422)


def calcular_ruta(puntos, ciudad):
    validar_solicitud(puntos, ciudad)
    paradas = len(puntos) - 1

    t0 = time.perf_counter()
    g = _cargar_grafo(puntos)
    t1 = time.perf_counter()

    nodos = _ajustar_a_calles(g, puntos)                       # 1. nodos en el mapa de calles
    artificial = _grafo_artificial(g, nodos)                   # 2-3. Dijkstra + grafo artificial
    t2 = time.perf_counter()

    orden, info = algoritmos.resolver_tsp(artificial.costos, OR_OPT_SEGMENTO_MAX)   # 4-5. Greedy + Or-opt
    t3 = time.perf_counter()

    secuencia = [0] + orden + [0]
    linea, metros = artificial.trazar(secuencia)               # 6. de vuelta al mapa real
    if len(linea) < 2:
        raise ErrorNegocio(
            "Las entregas están en el mismo cruce que el negocio. "
            "Sepáralas para poder trazar una ruta.", 422)
    t4 = time.perf_counter()

    log.info("ruta: grafo=%.2fs dijkstra=%.2fs tsp=%.3fs trazo=%.2fs",
             t1 - t0, t2 - t1, t3 - t2, t4 - t3)

    costo_greedy, costo_final = info["costo_greedy"], info["costo_final"]
    mejora = (costo_greedy - costo_final) / costo_greedy * 100 if costo_greedy > 0 else 0.0

    mov_min = costo_final / 60
    servicio_min = paradas * TIEMPO_SERVICIO_MIN
    return {
        "geometry": {"type": "LineString", "coordinates": linea},
        "orden": orden,
        "metodo": info["metodo"],
        "distancia_m": round(metros, 1),
        "duracion_movimiento_min": round(mov_min, 1),
        "tiempo_servicio_min": servicio_min,
        "tiempo_total_min": round(mov_min + servicio_min, 1),
        "paradas": paradas,
        "mejora_or_opt_pct": round(mejora, 1),
        "diagnostico_s": {"grafo": round(t1 - t0, 2), "dijkstra": round(t2 - t1, 2),
                          "tsp": round(t3 - t2, 3), "trazo": round(t4 - t3, 2)},
    }
