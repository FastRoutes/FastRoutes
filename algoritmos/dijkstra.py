import heapq
import math

INF = math.inf


def dijkstra(adj, origen, objetivos=None):
    """
    Nodos: u y v 
    adj: grafo dirigido
    Devuelve (tiempo, previo); 
    previo[v] = (u, metros_arista, geometria).
    Si se dan 'objetivos', se detiene al haberlos fijado a todos.
    """
    tiempo = {origen: 0.0}
    previo = {}
    pendientes = set(objetivos) if objetivos is not None else None
    cola = [(0.0, origen)]
    empujar, sacar, get = heapq.heappush, heapq.heappop, tiempo.get

    while cola:
        t, u = sacar(cola)
        if t > tiempo[u]:      
            continue
        if pendientes is not None:
            pendientes.discard(u)
            if not pendientes:
                break
        for v, dt, metros, geom in adj[u]:
            nuevo = t + dt
            if nuevo < get(v, INF):
                tiempo[v] = nuevo
                previo[v] = (u, metros, geom)
                empujar(cola, (nuevo, v))
    return tiempo, previo


def reconstruir_camino(previo, origen, destino):
    """Recorre nodos desde el origen hasta llegar al destino (actual) y devuelve la lista de geometrías y la distancia total en metros."""
    tramos, metros, actual = [], 0.0, destino
    while actual != origen:
        anterior, m, geom = previo[actual]
        tramos.append(geom)
        metros += m
        actual = anterior
    tramos.reverse()
    return tramos, metros


def aplanar(tramos):
    """Une los tramos individuales en una sola línea continua."""
    linea = []
    for geom in tramos:
        for x, y in (geom.coords if hasattr(geom, "coords") else geom):
            if not linea or linea[-1] != [x, y]:
                linea.append([x, y])
    return linea
