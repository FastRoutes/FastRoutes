from functools import lru_cache

# Velocidad (km/h) cuando la calle no trae 'maxspeed'
VELOCIDAD_POR_TIPO = {
    "motorway": 80, "trunk": 70, "primary": 50, "secondary": 40,
    "tertiary": 35, "unclassified": 30, "residential": 25,
    "living_street": 15, "service": 15,
}
VELOCIDAD_DEFECTO = 30
VELOCIDAD_MINIMA = 10


def _primero(valor):
    return valor[0] if isinstance(valor, list) else valor


@lru_cache(maxsize=None)
def _calcular(maxspeed, tipo):
    if isinstance(maxspeed, str):
        try:
            valor = float(maxspeed.split()[0])
            if "mph" in maxspeed:
                valor *= 1.609
            return max(valor, VELOCIDAD_MINIMA)
        except (ValueError, IndexError):
            pass
    return VELOCIDAD_POR_TIPO.get(str(tipo).replace("_link", ""), VELOCIDAD_DEFECTO)


def velocidad_kmh(datos):
    """Velocidad de una arista de osmnx (memoizada: hay pocas combinaciones distintas)."""
    return _calcular(_primero(datos.get("maxspeed")), _primero(datos.get("highway")))
