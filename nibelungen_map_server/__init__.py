
import os

from flask import Blueprint, Flask, jsonify

PACKDIR = os.path.abspath(os.path.dirname(__file__))

nibelungen_map = Blueprint('nibelungen_map', __name__)


def create_app(blueprint, url_prefix="/nibelungen-map"):
    app = Flask(__name__)
    app.secret_key = "anagramme"

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"success": False, "message": "Unknown page"})

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({"success": False, "message": "Internal error"})

    app.register_blueprint(blueprint, url_prefix=url_prefix)

    return app
