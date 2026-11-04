"""FastRoutes - Endpoints REST (/api)."""
from flask import Blueprint, jsonify, request
import logging
from werkzeug.exceptions import HTTPException
log = logging.getLogger(__name__)

import grafo
from config import MAX_PARADAS, PRECARGA_GRADOS, RADIO_MAX_ENTREGA_KM
from servicios import ErrorNegocio, calcular_ruta
from servicios.validaciones import validar_punto_precarga

bp = Blueprint("api", __name__, url_prefix="/api")

@bp.errorhandler(ErrorNegocio)
def error_negocio(e):
    return jsonify(error=e.mensaje), e.codigo

@bp.errorhandler(Exception)
def error_inesperado(e):
    if isinstance(e, HTTPException):
        return jsonify(error=e.description), e.code
    log.exception("Error no controlado")
    return jsonify(error="Error interno del servidor."), 500

def _cuerpo_json():
    datos = request.get_json(silent=True)
    return datos if isinstance(datos, dict) else {}


@bp.get("/config")
def configuracion():
    return jsonify(max_paradas=MAX_PARADAS, radio_max_km=RADIO_MAX_ENTREGA_KM)


@bp.get("/health")
def health():
    return jsonify(estado="ok")


@bp.post("/ruta")
def ruta():
    datos = _cuerpo_json()
    return jsonify(calcular_ruta(datos.get("puntos", []), datos.get("ciudad")))


@bp.post("/precargar")
def precargar():
    """Carga los datos en la memoria con anticipación mientras el usuario elige entregas."""
    datos = _cuerpo_json()
    punto = datos.get("punto")
    validar_punto_precarga(punto, datos.get("ciudad"))
    lng, lat = punto
    grafo.precargar(lat, lng, PRECARGA_GRADOS)
    return jsonify(estado="en_curso"), 202
