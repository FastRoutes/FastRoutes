"""Cálculo de la ruta óptima de un viaje almacén -> entregas."""
import logging
import time

import algoritmos
import grafo
from algoritmos import INF
from config import LIMITE_EXACTO, TIEMPO_SERVICIO_MIN

from .errores import ErrorNegocio
from .validaciones import caja_con_margen, validar_solicitud

log = logging.getLogger(__name__)


def _cargar_grafo(puntos):
    try:
        return grafo.obtener_grafo(*caja_con_margen(puntos))
    except Exception:
        log.exception("Error al cargar el grafo")
        raise ErrorNegocio("No se pudo descargar el mapa de calles. Revisa tu conexión.", 502)


def _dijkstra_por_nodo(adj, nodos):
    """Un Dijkstra por nodo distinto (los puntos que caen en el mismo cruce se reutilizan)."""
    unicos = set(nodos)
    return {n: algoritmos.dijkstra(adj, n, unicos - {n}) for n in unicos}


def _matriz_costos(nodos, resultados):
    n = len(nodos)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        tiempos = resultados[nodos[i]][0]
        for j in range(n):
            if nodos[i] != nodos[j]:
                C[i][j] = tiempos.get(nodos[j], INF)
                if C[i][j] == INF:
                    raise ErrorNegocio("Algún punto es inalcanzable por las calles. Mueve los puntos.", 422)
    return C


def _trazar(nodos, secuencia, resultados):
    """Devuelve (línea [[lng, lat], ...], metros totales) del circuito completo."""
    tramos, metros_total = [], 0.0
    for a, b in zip(secuencia, secuencia[1:]):
        if nodos[a] == nodos[b]:
            continue
        previo = resultados[nodos[a]][1]
        geoms, metros = algoritmos.reconstruir_camino(previo, nodos[a], nodos[b])
        tramos.extend(geoms)
        metros_total += metros
    return algoritmos.aplanar(tramos), metros_total


def calcular_ruta(puntos, ciudad):
    validar_solicitud(puntos, ciudad)
    paradas = len(puntos) - 1

    t0 = time.perf_counter()
    g = _cargar_grafo(puntos)
    t1 = time.perf_counter()

    nodos = [g.nodo_mas_cercano(lng, lat) for lng, lat in puntos]
    resultados = _dijkstra_por_nodo(g.adj, nodos)
    costos = _matriz_costos(nodos, resultados)
    t2 = time.perf_counter()

    orden, metodo = algoritmos.mejor_circuito(costos, LIMITE_EXACTO)
    secuencia = [0] + orden + [0]
    linea, metros = _trazar(nodos, secuencia, resultados)
    if len(linea) < 2:
        raise ErrorNegocio(
            "Las entregas están en el mismo cruce que el negocio. "
            "Sepáralas para poder trazar una ruta.", 422)
    segundos = sum(costos[a][b] for a, b in zip(secuencia, secuencia[1:]))
    t3 = time.perf_counter()

    log.info("ruta: grafo=%.2fs dijkstra=%.2fs orden+trazo=%.2fs", t1 - t0, t2 - t1, t3 - t2)

    mov_min = segundos / 60
    servicio_min = paradas * TIEMPO_SERVICIO_MIN
    return {
        "geometry": {"type": "LineString", "coordinates": linea},
        "orden": orden,
        "metodo": metodo,
        "distancia_m": round(metros, 1),
        "duracion_movimiento_min": round(mov_min, 1),
        "tiempo_servicio_min": servicio_min,
        "tiempo_total_min": round(mov_min + servicio_min, 1),
        "paradas": paradas,
        "diagnostico_s": {"grafo": round(t1 - t0, 2), "dijkstra": round(t2 - t1, 2),
                          "orden_y_trazo": round(t3 - t2, 2)},
    }
