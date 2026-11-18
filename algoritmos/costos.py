def costo_circuito(C, orden):
    """Costo del circuito almacén -> orden -> almacén sobre la matriz C."""
    secuencia = [0] + list(orden) + [0]
    return sum(C[a][b] for a, b in zip(secuencia, secuencia[1:]))
