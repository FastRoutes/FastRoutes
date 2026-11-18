from .costos import costo_circuito
from .greedy import greedy_aproximacion
from .or_opt import or_opt

METODO = "Greedy + Or-opt"


def resolver_tsp(C, max_segmento=3):
    """
    Resuelve el TSP asimétrico sobre el grafo artificial (matriz C):
    Greedy para una solución inicial rápida y Or-opt para mejorarla.

    Devuelve (orden, info). `orden` son las paradas sin el almacén;
    `info` lleva el método y los costos antes y después de Or-opt.
    """
    inicial = greedy_aproximacion(C)
    final = or_opt(C, inicial, max_segmento)
    return final, {
        "metodo": METODO,
        "costo_greedy": costo_circuito(C, inicial),
        "costo_final": costo_circuito(C, final),
    }
