"""Prueba de integración del caso de uso con una ciudad sintética (sin descargar nada)."""
import sys
import types
import unittest
from unittest import mock

try:
    import osmnx  # noqa: F401
except ImportError:                      # solo se necesita para importar el paquete grafo
    sys.modules["osmnx"] = types.ModuleType("osmnx")

import grafo
from grafo.modelo import Grafo
from servicios import ErrorNegocio, calcular_ruta

N, PASO, LAT0, LNG0 = 8, 0.002, -12.06, -77.06     # grilla de 8x8 calles dentro de Lima


def grilla():
    coords = {r * N + c: (LNG0 + c * PASO, LAT0 + r * PASO) for r in range(N) for c in range(N)}
    adj = {k: [] for k in coords}
    for r in range(N):
        for c in range(N):
            u = r * N + c
            for dr, dc in ((0, 1), (1, 0)):
                if r + dr < N and c + dc < N:
                    v = (r + dr) * N + (c + dc)
                    adj[u].append((v, 20.0, 220.0, [coords[u], coords[v]]))
                    adj[v].append((u, 20.0, 220.0, [coords[v], coords[u]]))
    return Grafo(adj, coords), coords


class TestCalcularRuta(unittest.TestCase):
    def setUp(self):
        self.g, self.coords = grilla()

    def _ruta(self, nodos):
        puntos = [[self.coords[n][0] + 0.0002, self.coords[n][1] + 0.0002] for n in nodos]
        with mock.patch.object(grafo, "obtener_grafo", return_value=self.g):
            return calcular_ruta(puntos, "Lima")

    def test_ruta_completa(self):
        r = self._ruta([0, 27, 45, 12, 60, 9])
        self.assertEqual(sorted(r["orden"]), [1, 2, 3, 4, 5])
        self.assertEqual(r["metodo"], "Greedy + Or-opt")
        self.assertEqual(r["paradas"], 5)
        self.assertGreaterEqual(r["mejora_or_opt_pct"], 0)
        coords = r["geometry"]["coordinates"]
        self.assertEqual(coords[0], coords[-1])                 # sale y regresa al negocio
        self.assertEqual(coords[0], list(self.coords[0]))
        self.assertGreater(r["distancia_m"], 0)
        self.assertAlmostEqual(r["tiempo_total_min"],
                               r["duracion_movimiento_min"] + r["tiempo_servicio_min"], delta=0.1)

    def test_una_sola_entrega(self):
        r = self._ruta([0, 63])
        self.assertEqual(r["orden"], [1])

    def test_mismo_cruce_que_el_negocio(self):
        with self.assertRaises(ErrorNegocio) as ctx:
            self._ruta([0, 0])
        self.assertEqual(ctx.exception.codigo, 422)

    def test_ciudad_invalida(self):
        with self.assertRaises(ErrorNegocio):
            calcular_ruta([[-77.0, -12.0], [-77.01, -12.01]], "Atlantis")


if __name__ == "__main__":
    unittest.main()
