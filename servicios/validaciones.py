"""Reglas de negocio para pedir la ruta."""
from config import CIUDADES, EXTENSION_MAX_GRADOS, MARGEN_GRADOS, MAX_PARADAS, RADIO_MAX_ENTREGA_KM
from grafo.geo import distancia_km
from .errores import ErrorNegocio

import math # Validación de números

def _numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)

def punto_valido(p):
    if not (isinstance(p, (list, tuple)) and len(p) == 2 and all(_numero(c) for c in p)):
        return False
    lng, lat = p
    return -180 <= lng <= 180 and -90 <= lat <= 90


def _datos_ciudad(ciudad):
    if not isinstance(ciudad, str) or ciudad not in CIUDADES:
        raise ErrorNegocio("Ciudad no soportada.")
    return CIUDADES[ciudad]

def _hay_fuera_de_ciudad(ciudad, puntos):
    lat_c, lng_c, radio = _datos_ciudad(ciudad)
    return any(distancia_km(lat_c, lng_c, lat, lng) > radio for lng, lat in puntos)

def validar_punto_precarga(punto, ciudad):
    if not punto_valido(punto):
        raise ErrorNegocio("Punto inválido.")
    if _hay_fuera_de_ciudad(ciudad, [punto]):
        raise ErrorNegocio(f"El punto debe estar dentro de {ciudad}.")


def validar_solicitud(puntos, ciudad):
    """Error de Negocio si la solicitud incumple alguna regla."""
    if not isinstance(puntos, list) or not all(punto_valido(p) for p in puntos):
        raise ErrorNegocio("Formato de puntos inválido.")
    if len(puntos) < 2:
        raise ErrorNegocio("Selecciona el almacén y al menos 1 entrega.")
    if len(puntos) - 1 > MAX_PARADAS:
        raise ErrorNegocio(f"Máximo {MAX_PARADAS} paradas por viaje.")

    if _hay_fuera_de_ciudad(ciudad, puntos):
        raise ErrorNegocio(f"Todos los puntos deben estar dentro de {ciudad}.")
    lat_c, lng_c, radio = CIUDADES[ciudad]
    if any(distancia_km(lat_c, lng_c, lat, lng) > radio for lng, lat in puntos):
        raise ErrorNegocio(f"Todos los puntos deben estar dentro de {ciudad}.")

    alm_lng, alm_lat = puntos[0]
    if any(distancia_km(alm_lat, alm_lng, lat, lng) > RADIO_MAX_ENTREGA_KM
           for lng, lat in puntos[1:]):
        raise ErrorNegocio(f"Las entregas deben estar a máximo {RADIO_MAX_ENTREGA_KM} km del negocio.")

    lngs, lats = zip(*puntos)
    if (max(lngs) - min(lngs) > EXTENSION_MAX_GRADOS
            or max(lats) - min(lats) > EXTENSION_MAX_GRADOS):
        raise ErrorNegocio("Los puntos están demasiado separados.")


def caja_con_margen(puntos):
    """(norte, sur, este, oeste) que contiene todos los puntos más un margen."""
    lngs, lats = zip(*puntos)
    return (max(lats) + MARGEN_GRADOS, min(lats) - MARGEN_GRADOS,
            max(lngs) + MARGEN_GRADOS, min(lngs) - MARGEN_GRADOS)
