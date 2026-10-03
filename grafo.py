"""
FastRoutes - Grafo vial dirigido

Descarga la red de calles de OpenStreetMap (osmnx) solo para la zona
donde están los puntos y la convierte en una lista de adyacencia propia:

    adj[nodo] = [(vecino, tiempo_s, metros, geometria), ...]

Las aristas respetan el sentido del tránsito (calles de un solo sentido).
"""
import math

import osmnx as ox

# Velocidad (km/h) cuando la calle no trae 'maxspeed'
VELOCIDAD_POR_TIPO = {
    "motorway": 80, "trunk": 70, "primary": 50, "secondary": 40,
    "tertiary": 35, "unclassified": 30, "residential": 25,
    "living_street": 15, "service": 15,
}
VELOCIDAD_MINIMA = 10

_cache = {}  # últimos grafos usados en memoria (además del caché en disco de osmnx)


def _velocidad_kmh(datos):
    maxspeed = datos.get("maxspeed")
    if isinstance(maxspeed, list):
        maxspeed = maxspeed[0]
    if isinstance(maxspeed, str):
        try:
            valor = float(maxspeed.split()[0])
            if "mph" in maxspeed:
                valor *= 1.609
            return max(valor, VELOCIDAD_MINIMA)
        except ValueError:
            pass
    tipo = datos.get("highway")
    if isinstance(tipo, list):
        tipo = tipo[0]
    return VELOCIDAD_POR_TIPO.get(str(tipo).replace("_link", ""), 30)


def obtener_grafo(norte, sur, este, oeste):
    """Devuelve (adj, coords) para la caja indicada. coords[nodo] = (lng, lat)."""
    clave = tuple(round(x, 3) for x in (norte, sur, este, oeste))
    if clave in _cache:
        return _cache[clave]

    G = ox.graph_from_bbox((oeste, sur, este, norte), network_type="drive")
    # Nos quedamos con la parte donde se puede ir y volver a cualquier nodo
    G = ox.truncate.largest_component(G, strongly=True)

    coords = {n: (d["x"], d["y"]) for n, d in G.nodes(data=True)}
    adj = {n: [] for n in G.nodes}
    for u, v, datos in G.edges(data=True):
        if u == v:
            continue
        metros = float(datos.get("length", 0.0))
        tiempo = metros / (_velocidad_kmh(datos) / 3.6)
        if "geometry" in datos:
            geom = list(datos["geometry"].coords)
        else:
            geom = [coords[u], coords[v]]
        adj[u].append((v, tiempo, metros, geom))

    if len(_cache) >= 3:
        _cache.pop(next(iter(_cache)))
    _cache[clave] = (adj, coords)
    return adj, coords


def nodo_mas_cercano(coords, lng, lat):
    """Cruce más cercano al punto (búsqueda lineal, distancia aproximada)."""
    k = math.cos(math.radians(lat))
    mejor, mejor_d = None, math.inf
    for nodo, (x, y) in coords.items():
        d = (x - lng) ** 2 * k * k + (y - lat) ** 2
        if d < mejor_d:
            mejor, mejor_d = nodo, d
    return mejor


def distancia_km(lat1, lng1, lat2, lng2):
    """Haversine."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))
