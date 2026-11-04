import math
import numpy as np
class Grafo:

    __slots__ = ("adj", "ids", "xs", "ys")

    def __init__(self, adj, coords):
        self.adj = adj
        self.ids = list(coords)
        arr = np.array([coords[n] for n in self.ids], dtype=float)
        self.xs, self.ys = arr[:, 0], arr[:, 1]

    def nodo_y_distancia(self, lng, lat):
        k = math.cos(math.radians(lat))
        d = ((self.xs - lng) * k) ** 2 + (self.ys - lat) ** 2
        i = int(d.argmin())
        return self.ids[i], math.sqrt(d[i]) * 111_320      # metros aprox.

    def nodo_mas_cercano(self, lng, lat):
        return self.nodo_y_distancia(lng, lat)[0]
