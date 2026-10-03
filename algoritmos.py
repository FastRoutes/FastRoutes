"""
FastRoutes - Algoritmos propios

- dijkstra: caminos mínimos sobre el grafo dirigido (cola de prioridad / heapq)
- held_karp: orden óptimo de visitas (exacto) para pocas paradas
- vecino_mas_cercano + dos_opt: orden de visitas aproximado para más paradas

Convención de la matriz de costos C (n+1 x n+1):
    índice 0 = almacén, 1..n = paradas en el orden en que se hizo clic.
    C[i][j] = tiempo (s) de ir de i a j respetando el sentido de las calles.
    Es asimétrica: ir de i a j no cuesta lo mismo que de j a i.
"""
import heapq
import math

INF = math.inf


# ---------------------------------------------------------------- Dijkstra
def dijkstra(adj, origen, objetivos=None):
    """
    adj: {nodo: [(vecino, tiempo_s, metros, geometria), ...]}  (grafo dirigido)
    Devuelve (tiempo, metros, previo) como diccionarios.
    Si se dan 'objetivos', se detiene al haberlos fijado a todos.
    """
    tiempo = {origen: 0.0}
    metros = {origen: 0.0}
    previo = {}
    pendientes = set(objetivos) if objetivos is not None else None

    cola = [(0.0, origen)]
    visitados = set()

    while cola:
        t, u = heapq.heappop(cola)
        if u in visitados:
            continue
        visitados.add(u)

        if pendientes is not None:
            pendientes.discard(u)
            if not pendientes:
                break

        for v, t_arista, m_arista, geom in adj[u]:
            nuevo = t + t_arista
            if nuevo < tiempo.get(v, INF):
                tiempo[v] = nuevo
                metros[v] = metros[u] + m_arista
                previo[v] = (u, geom)
                heapq.heappush(cola, (nuevo, v))

    return tiempo, metros, previo


def reconstruir_camino(previo, origen, destino):
    """Lista de geometrías (una por arista) desde origen hasta destino."""
    tramos = []
    actual = destino
    while actual != origen:
        anterior, geom = previo[actual]
        tramos.append(geom)
        actual = anterior
    tramos.reverse()
    return tramos


# ------------------------------------------------------ Orden de visitas
def costo_circuito(C, orden):
    secuencia = [0] + list(orden) + [0]
    return sum(C[a][b] for a, b in zip(secuencia, secuencia[1:]))


def held_karp(C):
    """Solución exacta (programación dinámica con bitmask). O(n^2 * 2^n)."""
    n = len(C) - 1
    if n <= 1:
        return list(range(1, n + 1))

    # dp[(mask, j)] = (costo mínimo, nodo previo): salir de 0, visitar 'mask', terminar en j
    dp = {}
    for j in range(1, n + 1):
        dp[(1 << (j - 1), j)] = (C[0][j], 0)

    for mask in range(1, 1 << n):
        for j in range(1, n + 1):
            if not mask & (1 << (j - 1)) or (mask, j) not in dp:
                continue
            costo = dp[(mask, j)][0]
            for k in range(1, n + 1):
                if mask & (1 << (k - 1)):
                    continue
                nueva = mask | (1 << (k - 1))
                nc = costo + C[j][k]
                if nc < dp.get((nueva, k), (INF, 0))[0]:
                    dp[(nueva, k)] = (nc, j)

    completo = (1 << n) - 1
    ultimo = min(range(1, n + 1), key=lambda j: dp[(completo, j)][0] + C[j][0])

    orden, mask, j = [], completo, ultimo
    while j != 0:
        orden.append(j)
        previo = dp[(mask, j)][1]
        mask &= ~(1 << (j - 1))
        j = previo
    orden.reverse()
    return orden


def vecino_mas_cercano(C):
    n = len(C) - 1
    restantes = set(range(1, n + 1))
    orden, actual = [], 0
    while restantes:
        siguiente = min(restantes, key=lambda j: C[actual][j])
        orden.append(siguiente)
        restantes.remove(siguiente)
        actual = siguiente
    return orden


def dos_opt(C, orden):
    """Mejora local: invierte tramos mientras reduzca el costo total."""
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


def mejor_circuito(C, limite_exacto=12):
    """Devuelve (orden de paradas, nombre del método)."""
    n = len(C) - 1
    if n <= limite_exacto:
        return held_karp(C), "exacto (Held-Karp)"
    return dos_opt(C, vecino_mas_cercano(C)), "aproximado (vecino más cercano + 2-opt)"
