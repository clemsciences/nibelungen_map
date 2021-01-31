
import os

from flask import Blueprint, Flask, jsonify

PACKDIR = os.getcwd()

nibelungen_map = Blueprint('nibelungen_map', __name__)


def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.secret_key = "anagramme"

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"success": False, "message": "Unknown page"})

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"success": False, "message": "Internal error"})

    app.register_blueprint(nibelungen_map, url_prefix="/nibelungen-map")

    return app
