"""Reglas de negocio para pedir la ruta."""
from config import CIUDADES, EXTENSION_MAX_GRADOS, MARGEN_GRADOS, MAX_PARADAS
from grafo.geo import distancia_km

from .errores import ErrorNegocio


def _numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def punto_valido(p):
    return isinstance(p, (list, tuple)) and len(p) == 2 and all(_numero(c) for c in p)


def validar_solicitud(puntos, ciudad):
    """Error de Negocio si la solicitud incumple alguna regla."""
    if not isinstance(puntos, list) or not all(punto_valido(p) for p in puntos):
        raise ErrorNegocio("Formato de puntos inválido.")
    if len(puntos) < 2:
        raise ErrorNegocio("Selecciona el almacén y al menos 1 entrega.")
    if len(puntos) - 1 > MAX_PARADAS:
        raise ErrorNegocio(f"Máximo {MAX_PARADAS} paradas por viaje.")

    if ciudad not in CIUDADES:
        raise ErrorNegocio("Ciudad no soportada.")
    lat_c, lng_c, radio = CIUDADES[ciudad]
    if any(distancia_km(lat_c, lng_c, lat, lng) > radio for lng, lat in puntos):
        raise ErrorNegocio(f"Todos los puntos deben estar dentro de {ciudad}.")

    lngs, lats = zip(*puntos)
    if (max(lngs) - min(lngs) > EXTENSION_MAX_GRADOS
            or max(lats) - min(lats) > EXTENSION_MAX_GRADOS):
        raise ErrorNegocio("Los puntos están demasiado separados.")


def caja_con_margen(puntos):
    """(norte, sur, este, oeste) que contiene todos los puntos más un margen."""
    lngs, lats = zip(*puntos)
    return (max(lats) + MARGEN_GRADOS, min(lats) - MARGEN_GRADOS,
            max(lngs) + MARGEN_GRADOS, min(lngs) - MARGEN_GRADOS)
