"""FastRoutes - Servidor Flask (fábrica de la aplicación y archivos estáticos)."""
from flask import Flask, send_from_directory

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
    app.run(debug=True, port=5000, threaded=True)
