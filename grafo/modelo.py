import math

import numpy as np


class Grafo:
    """
    adj[nodo] = [(vecino, tiempo_s, metros, geometria), ...]   (dirigido)
    'geometria' es un LineString de shapely o una tupla de dos puntos (lng, lat).
    """
    __slots__ = ("adj", "ids", "xs", "ys")

    def __init__(self, adj, coords):
        self.adj = adj
        self.ids = list(coords)
        arr = np.array([coords[n] for n in self.ids], dtype=float)
        self.xs, self.ys = arr[:, 0], arr[:, 1]

    def nodo_mas_cercano(self, lng, lat):
        """Cruce más cercano (vectorizado con numpy; distancia equirectangular)."""
        k = math.cos(math.radians(lat))
        d = ((self.xs - lng) * k) ** 2 + (self.ys - lat) ** 2
        return self.ids[int(d.argmin())]
