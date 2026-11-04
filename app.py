"""FastRoutes - Servidor Flask (creación de la aplicación y archivos estáticos)."""
from flask import Flask, send_from_directory
import logging, os
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

from api import bp
from config import FRONTEND_DIR


def crear_app():
    app = Flask(__name__, static_folder=None)
    app.register_blueprint(bp)

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:archivo>")
    def estaticos(archivo):
        return send_from_directory(FRONTEND_DIR, archivo)

    return app


app = crear_app()

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1", port=5000, threaded=True)
