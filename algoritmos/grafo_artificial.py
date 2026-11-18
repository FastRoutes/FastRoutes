"""Grafo artificial: los puntos seleccionados, con sus caminos mínimos como aristas."""
from .dijkstra import INF, aplanar, dijkstra, reconstruir_camino


class PuntoInalcanzable(Exception):
    """No existe camino por las calles entre dos puntos seleccionados."""

    def __init__(self, origen, destino):
        super().__init__(f"No hay camino del punto {origen} al punto {destino}.")
        self.origen = origen
        self.destino = destino


class GrafoArtificial:
    """
    Grafo completo y dirigido sobre los puntos seleccionados (índice 0 = almacén).

    - Vértices: los puntos seleccionados, ya ajustados a su nodo de calle más cercano.
    - Arista i -> j: el camino mínimo (Dijkstra) de nodos[i] a nodos[j]. Su peso es el
      tiempo de viaje, por eso la matriz `costos` es asimétrica (calles de un solo sentido).
    - Cada arista conserva su camino real de calles, que se usa en `trazar` para llevar
      el tour resuelto de vuelta al mapa.
    """

    def __init__(self, nodos, resultados):
        """
        nodos: nodos[i] = nodo de calle del punto i.
        resultados: {nodo: (tiempo, previo)} devuelto por Dijkstra para cada nodo distinto.
        """
        self.nodos = list(nodos)
        self._resultados = resultados
        self.costos = self._construir_matriz()

    @classmethod
    def desde_calles(cls, adj, nodos):
        """Ejecuta un Dijkstra por nodo distinto (puntos en el mismo cruce se reutilizan)."""
        unicos = set(nodos)
        resultados = {n: dijkstra(adj, n, unicos - {n}) for n in unicos}
        return cls(nodos, resultados)

    def __len__(self):
        return len(self.nodos)

    def _construir_matriz(self):
        n = len(self.nodos)
        C = [[0.0] * n for _ in range(n)]
        for i in range(n):
            tiempos = self._resultados[self.nodos[i]][0]
            for j in range(n):
                if self.nodos[i] == self.nodos[j]:
                    continue
                tiempo = tiempos.get(self.nodos[j], INF)
                if tiempo == INF:
                    raise PuntoInalcanzable(i, j)
                C[i][j] = tiempo
        return C

    def trazar(self, secuencia):
        """
        Cambia cada arista artificial del tour por su camino real de calles.
        Devuelve (línea [[lng, lat], ...], metros totales).
        """
        tramos, metros_total = [], 0.0
        for a, b in zip(secuencia, secuencia[1:]):
            if self.nodos[a] == self.nodos[b]:
                continue
            previo = self._resultados[self.nodos[a]][1]
            geoms, metros = reconstruir_camino(previo, self.nodos[a], self.nodos[b])
            tramos.extend(geoms)
            metros_total += metros
        return aplanar(tramos), metros_total
