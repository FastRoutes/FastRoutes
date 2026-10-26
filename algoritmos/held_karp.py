from .dijkstra import INF


def held_karp(C):
    """Encuentra la ruta optima con programación dinámica."""
    n = len(C) - 1
    if n <= 1:
        return list(range(1, n + 1))

    total = 1 << n
    # dp[mask][j]: costo mínimo de salir de 0, visitar 'mask' y terminar en la parada j+1
    dp = [[INF] * n for _ in range(total)]
    padre = [[-1] * n for _ in range(total)]
    for j in range(n):
        dp[1 << j][j] = C[0][j + 1]

    for mask in range(1, total):
        fila = dp[mask]
        for j in range(n):
            costo = fila[j]
            if costo == INF:
                continue
            cj = C[j + 1]
            for k in range(n):
                bit = 1 << k
                if mask & bit:
                    continue
                nuevo = costo + cj[k + 1]
                destino = dp[mask | bit]
                if nuevo < destino[k]:
                    destino[k] = nuevo
                    padre[mask | bit][k] = j

    completo = total - 1
    j = min(range(n), key=lambda x: dp[completo][x] + C[x + 1][0])
    orden, mask = [], completo
    while j != -1:
        orden.append(j + 1)
        previo = padre[mask][j]
        mask &= ~(1 << j)
        j = previo
    return orden[::-1]
