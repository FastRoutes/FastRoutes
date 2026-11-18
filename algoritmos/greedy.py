def greedy_aproximacion(C):
    """
    Heurística Greedy (aproximación) para el TSP asimétrico.

    Ordena todos los arcos i -> j por costo y los va aceptando de menor a mayor,
    descartando los que:
      - ya tienen otro arco saliendo de i,
      - ya tienen otro arco entrando a j,
      - cerrarían un subciclo antes de tener el camino completo.
    Al reunir n arcos (para n+1 puntos) queda un único camino hamiltoniano; el arco que
    lo cierra es el que va del último al primero. El ciclo se rota para empezar en el
    almacén (índice 0).

    Devuelve el orden de las paradas (sin el almacén).
    """
    N = len(C)
    if N <= 2:
        return list(range(1, N))

    arcos = sorted((C[i][j], i, j) for i in range(N) for j in range(N) if i != j)

    siguiente = [None] * N     # siguiente[u] = v  si se aceptó el arco u -> v
    entra = [False] * N        # entra[v] = True   si algún arco ya llega a v
    inicio = list(range(N))    # inicio[t]: primer nodo de la cadena que termina en t
    fin = list(range(N))       # fin[h]:    último nodo de la cadena que empieza en h

    aceptados = 0
    for _, u, v in arcos:
        if siguiente[u] is not None or entra[v]:
            continue
        if inicio[u] == v:     # v -> ... -> u ya existe: u -> v cerraría un subciclo
            continue
        siguiente[u] = v
        entra[v] = True
        cabeza, cola = inicio[u], fin[v]
        fin[cabeza] = cola
        inicio[cola] = cabeza
        aceptados += 1
        if aceptados == N - 1:
            break

    # Cierra el ciclo: el único nodo sin salida enlaza con el único sin entrada.
    cola = siguiente.index(None)
    cabeza = entra.index(False)
    siguiente[cola] = cabeza

    orden, actual = [], siguiente[0]
    while actual != 0:
        orden.append(actual)
        actual = siguiente[actual]
    return orden
