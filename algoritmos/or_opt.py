def or_opt(C, orden, max_segmento=3):
    """
    Tour improvement Or-opt, apto para TSP asimétrico.

    Toma un segmento de 1 a `max_segmento` paradas consecutivas y lo reinserta en otra
    posición del circuito SIN invertirlo (invertir cambiaría el sentido de cada arco, y
    en una matriz asimétrica eso altera el costo del propio segmento; 2-opt por eso no
    sirve aquí). Cada movimiento se evalúa en O(1) con la variación de los 3 arcos
    afectados y se acepta si reduce el costo. Se repite hasta que ningún movimiento mejora.

    El almacén (índice 0) permanece fijo al inicio del circuito.
    Devuelve el nuevo orden de las paradas (sin el almacén).
    """
    tour = [0] + list(orden)          # circuito cíclico; el arco final vuelve a tour[0]
    m = len(tour)
    if m < 3:
        return list(orden)

    EPS = 1e-9
    mejoro = True
    while mejoro:
        mejoro = False
        for k in range(1, min(max_segmento, m - 2) + 1):
            for i in range(1, m - k + 1):
                seg = tour[i:i + k]
                ant, sig = tour[i - 1], tour[(i + k) % m]
                primero, ultimo = seg[0], seg[-1]
                ahorro = C[ant][primero] + C[ultimo][sig] - C[ant][sig]

                resto = tour[:i] + tour[i + k:]
                n_resto = len(resto)
                mejor_delta, mejor_pos = -EPS, None
                for j in range(n_resto):
                    if j == i - 1:    # la posición original: no es un movimiento
                        continue
                    a, b = resto[j], resto[(j + 1) % n_resto]
                    delta = C[a][primero] + C[ultimo][b] - C[a][b] - ahorro
                    if delta < mejor_delta:
                        mejor_delta, mejor_pos = delta, j
                if mejor_pos is not None:
                    tour = resto[:mejor_pos + 1] + seg + resto[mejor_pos + 1:]
                    mejoro = True
                    break
            if mejoro:
                break
    return tour[1:]
