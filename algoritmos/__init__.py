"""
FastRoutes - Algoritmos propios

Flujo de optimización:
    1. Dijkstra desde cada nodo seleccionado   -> caminos mínimos entre todos ellos.
    2. GrafoArtificial                         -> grafo completo dirigido cuyas aristas son
                                                  esos caminos mínimos (aquí se resuelve el TSP).
    3. greedy_aproximacion                     -> solución inicial rápida del TSP asimétrico.
    4. or_opt                                  -> mejora del tour (válida para TSP asimétrico).
    5. GrafoArtificial.trazar                  -> cada arista del tour se cambia por su
                                                  camino real de calles.

Convención de la matriz de costos C (n+1 x n+1):
    índice 0 = almacén.
    n = paradas en el orden en que se hizo clic.
    C[i][j] = tiempo de i a j respetando el sentido de las calles (asimétrica).
"""
from .costos import costo_circuito
from .dijkstra import INF, aplanar, dijkstra, reconstruir_camino
from .grafo_artificial import GrafoArtificial, PuntoInalcanzable
from .greedy import greedy_aproximacion
from .or_opt import or_opt
from .tsp import resolver_tsp

__all__ = ["INF", "GrafoArtificial", "PuntoInalcanzable", "aplanar", "costo_circuito",
           "dijkstra", "greedy_aproximacion", "or_opt", "reconstruir_camino", "resolver_tsp"]
