"""
FastRoutes - Algoritmos propios

Convención de la matriz de costos C (n+1 x n+1):
    índice 0 = almacén, 1..n = paradas en el orden en que se hizo clic.
    C[i][j] = tiempo (s) de i a j respetando el sentido de las calles (asimétrica).
"""
from .circuito import mejor_circuito
from .dijkstra import INF, aplanar, dijkstra, reconstruir_camino
from .held_karp import held_karp
from .heuristicas import costo_circuito, dos_opt, vecino_mas_cercano

__all__ = ["INF", "aplanar", "costo_circuito", "dijkstra", "dos_opt", "held_karp",
           "mejor_circuito", "reconstruir_camino", "vecino_mas_cercano"]
