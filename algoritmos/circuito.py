from .held_karp import held_karp
from .heuristicas import dos_opt, vecino_mas_cercano


def mejor_circuito(C, limite_exacto=12):
    """Devuelve el orden de paradas y el nombre del método."""
    if len(C) - 1 <= limite_exacto:
        return held_karp(C), "exacto (método Held-Karp)"
    return dos_opt(C, vecino_mas_cercano(C)), "aproximado (vecino más cercano + 2-opt)"
