import osmnx as ox

from .modelo import Grafo
from .velocidades import velocidad_kmh


def descargar(norte, sur, este, oeste):
    G = ox.graph_from_bbox((oeste, sur, este, norte), network_type="drive")
    G = ox.truncate.largest_component(G, strongly=True)
    return a_grafo(G)


def a_grafo(G):
    coords = {n: (d["x"], d["y"]) for n, d in G.nodes(data=True)}

    mejores = {}
    for u, v, datos in G.edges(data=True):
        if u == v:
            continue
        metros = float(datos.get("length", 0.0))
        tiempo = metros / (velocidad_kmh(datos) / 3.6)
        if (u, v) not in mejores or tiempo < mejores[(u, v)][0]:
            geom = datos["geometry"] if "geometry" in datos else (coords[u], coords[v])
            mejores[(u, v)] = (tiempo, metros, geom)

    adj = {n: [] for n in G.nodes}
    for (u, v), (tiempo, metros, geom) in mejores.items():
        adj[u].append((v, tiempo, metros, geom))
    return Grafo(adj, coords)
