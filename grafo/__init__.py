import logging
import math
import threading

from .cache import CacheGrafos
from .construccion import descargar
from .geo import distancia_km
from .modelo import Grafo

__all__ = ["Grafo", "distancia_km", "obtener_grafo", "precargar"]

log = logging.getLogger(__name__)
PASO_GRADOS = 0.01  

_cache = CacheGrafos(capacidad=4)
_candado_descarga = threading.Lock()  


def _alinear(norte, sur, este, oeste):
    f = PASO_GRADOS
    return (round(math.ceil(norte / f) * f, 4), round(math.floor(sur / f) * f, 4),
            round(math.ceil(este / f) * f, 4), round(math.floor(oeste / f) * f, 4))


def obtener_grafo(norte, sur, este, oeste):
    caja = (norte, sur, este, oeste)
    grafo = _cache.buscar(caja)
    if grafo:
        return grafo
    with _candado_descarga:
        grafo = _cache.buscar(caja) 
        if grafo:
            return grafo
        ampliada = _alinear(*caja)
        grafo = descargar(*ampliada)
        _cache.guardar(ampliada, grafo)
        return grafo


def _precargar_seguro(*caja):
    try:
        obtener_grafo(*caja)
    except Exception:
        log.exception("Falló la precarga del mapa")


def precargar(lat, lng, radio_grados):
    caja = (lat + radio_grados, lat - radio_grados, lng + radio_grados, lng - radio_grados)
    threading.Thread(target=_precargar_seguro, args=caja, daemon=True).start()
