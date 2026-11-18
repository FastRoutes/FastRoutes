import itertools
import random
import unittest

from algoritmos import (INF, GrafoArtificial, PuntoInalcanzable, costo_circuito,
                        greedy_aproximacion, or_opt, resolver_tsp)


def matriz_asimetrica(n_paradas, semilla):
    rnd = random.Random(semilla)
    N = n_paradas + 1
    return [[0.0 if i == j else rnd.uniform(1, 100) for j in range(N)] for i in range(N)]


def optimo_fuerza_bruta(C):
    paradas = range(1, len(C))
    return min(costo_circuito(C, p) for p in itertools.permutations(paradas))


class TestGreedy(unittest.TestCase):
    def test_devuelve_permutacion_de_las_paradas(self):
        for n in range(1, 13):
            C = matriz_asimetrica(n, semilla=n)
            self.assertEqual(sorted(greedy_aproximacion(C)), list(range(1, n + 1)))

    def test_casos_minimos(self):
        self.assertEqual(greedy_aproximacion([[0.0]]), [])
        self.assertEqual(greedy_aproximacion([[0, 5], [7, 0]]), [1])

    def test_respeta_el_sentido_de_los_arcos(self):
        # Ciclo dirigido barato 0 -> 2 -> 1 -> 3 -> 0 (el resto cuesta mucho).
        C = [[0, 90, 1, 90], [90, 0, 90, 1], [90, 1, 0, 90], [1, 90, 90, 0]]
        self.assertEqual(greedy_aproximacion(C), [2, 1, 3])


class TestOrOpt(unittest.TestCase):
    def test_mejora_un_tour_malo_en_una_linea(self):
        C = [[abs(i - j) for j in range(5)] for i in range(5)]
        self.assertEqual(costo_circuito(C, [2, 1, 3, 4]), 10)
        self.assertEqual(costo_circuito(C, or_opt(C, [2, 1, 3, 4])), 8)

    def test_nunca_empeora_y_conserva_las_paradas(self):
        for semilla in range(40):
            n = 3 + semilla % 12
            C = matriz_asimetrica(n, semilla)
            inicial = list(range(1, n + 1))
            random.Random(semilla).shuffle(inicial)
            final = or_opt(C, inicial)
            self.assertEqual(sorted(final), list(range(1, n + 1)))
            self.assertLessEqual(costo_circuito(C, final), costo_circuito(C, inicial) + 1e-9)

    def test_no_invierte_segmentos(self):
        # Con costos asimétricos, el segmento (1, 2) solo es barato en ese sentido.
        C = [[0, 1, 50, 50], [50, 0, 1, 1], [50, 50, 0, 1], [1, 50, 50, 0]]
        final = or_opt(C, [3, 1, 2])
        self.assertEqual(costo_circuito(C, final), 4)
        self.assertLess(final.index(1), final.index(2))

    def test_entradas_pequenas(self):
        self.assertEqual(or_opt([[0.0]], []), [])
        self.assertEqual(or_opt([[0, 1], [2, 0]], [1]), [1])


class TestTSP(unittest.TestCase):
    def test_cerca_del_optimo_en_instancias_pequenas(self):
        for semilla in range(25):
            n = 4 + semilla % 4          # hasta 7 paradas
            C = matriz_asimetrica(n, semilla)
            orden, info = resolver_tsp(C)
            optimo = optimo_fuerza_bruta(C)
            self.assertEqual(sorted(orden), list(range(1, n + 1)))
            self.assertGreaterEqual(info["costo_final"], optimo - 1e-9)
            self.assertLessEqual(info["costo_final"], info["costo_greedy"] + 1e-9)
            self.assertAlmostEqual(info["costo_final"], costo_circuito(C, orden))
            self.assertLessEqual(info["costo_final"], optimo * 1.5)


def _calle(u, v, tiempo, metros, coords):
    return (v, tiempo, metros, [coords[u], coords[v]])


class TestGrafoArtificial(unittest.TestCase):
    def setUp(self):
        # Ciclo de un solo sentido 0 -> 1 -> 2 -> 3 -> 0 (10 s y 100 m por calle).
        self.coords = {0: (0.0, 0.0), 1: (1.0, 0.0), 2: (1.0, 1.0), 3: (0.0, 1.0)}
        self.adj = {u: [_calle(u, (u + 1) % 4, 10.0, 100.0, self.coords)] for u in range(4)}

    def test_costos_son_caminos_minimos_y_asimetricos(self):
        ga = GrafoArtificial.desde_calles(self.adj, [0, 2, 1])
        C = ga.costos
        self.assertEqual(C[0][1], 20.0)     # 0 -> 2
        self.assertEqual(C[1][0], 20.0)     # 2 -> 0
        self.assertEqual(C[0][2], 10.0)     # 0 -> 1
        self.assertEqual(C[2][0], 30.0)     # 1 -> 0 (da toda la vuelta)
        self.assertNotEqual(C[0][2], C[2][0])

    def test_trazar_cambia_aristas_por_caminos_reales(self):
        ga = GrafoArtificial.desde_calles(self.adj, [0, 2, 1])
        linea, metros = ga.trazar([0, 2, 1, 0])      # 0 -> 1 -> 2 -> 3 -> 0
        self.assertEqual(metros, 400.0)
        self.assertEqual(linea[0], [0.0, 0.0])
        self.assertEqual(linea[-1], [0.0, 0.0])
        self.assertEqual(len(linea), 5)

    def test_puntos_en_el_mismo_cruce_cuestan_cero(self):
        ga = GrafoArtificial.desde_calles(self.adj, [0, 0, 2])
        self.assertEqual(ga.costos[0][1], 0.0)
        self.assertEqual(ga.costos[1][0], 0.0)

    def test_punto_inalcanzable(self):
        adj = {0: [_calle(0, 1, 5.0, 50.0, self.coords)], 1: [], 2: []}
        with self.assertRaises(PuntoInalcanzable):
            GrafoArtificial.desde_calles(adj, [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
