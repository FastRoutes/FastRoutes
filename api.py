"""FastRoutes - Endpoints REST (/api)."""
from flask import Blueprint, jsonify, request

import grafo
from config import PRECARGA_GRADOS
from servicios import ErrorNegocio, calcular_ruta
from servicios.validaciones import punto_valido

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.get("/health")
def health():
    return jsonify(estado="ok")


@bp.post("/ruta")
def ruta():
    datos = request.get_json(silent=True) or {}
    try:
        return jsonify(calcular_ruta(datos.get("puntos", []), datos.get("ciudad")))
    except ErrorNegocio as e:
        return jsonify(error=e.mensaje), e.codigo


@bp.post("/precargar")
def precargar():
    """Calienta el caché del mapa alrededor del almacén mientras el usuario elige entregas."""
    punto = (request.get_json(silent=True) or {}).get("punto")
    if not punto_valido(punto):
        return jsonify(error="Punto inválido."), 400
    lng, lat = punto
    grafo.precargar(lat, lng, PRECARGA_GRADOS)
    return jsonify(estado="en_curso"), 202
