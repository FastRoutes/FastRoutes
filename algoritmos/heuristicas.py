def costo_circuito(C, orden):
    secuencia = [0] + list(orden) + [0]
    return sum(C[a][b] for a, b in zip(secuencia, secuencia[1:]))


def vecino_mas_cercano(C):
    restantes = set(range(1, len(C)))
    orden, actual = [], 0
    while restantes:
        siguiente = min(restantes, key=lambda j: C[actual][j])
        orden.append(siguiente)
        restantes.remove(siguiente)
        actual = siguiente
    return orden


def dos_opt(C, orden):
    """Mejora local: invierte tramos mientras reduzca el costo total. Hola Fabri"""
    mejor = list(orden)
    mejor_costo = costo_circuito(C, mejor)
    mejoro = True
    while mejoro:
        mejoro = False
        for i in range(len(mejor) - 1):
            for j in range(i + 1, len(mejor)):
                candidato = mejor[:i] + mejor[i:j + 1][::-1] + mejor[j + 1:]
                costo = costo_circuito(C, candidato)
                if costo < mejor_costo - 1e-9:
                    mejor, mejor_costo, mejoro = candidato, costo, True
    return mejor
