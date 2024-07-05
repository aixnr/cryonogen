from flask import Flask, jsonify
from flask_cors import CORS

from .vial_manifest import Vial
from .box_manifest import Box


def create_app() -> Flask:
    # Initialize the app
    app = Flask(__name__)
    app.debug = False
    CORS(app)

    # The route for all boxes (listing)
    @app.route("/boxes")
    def return_all_boxes():
        payload = Box().return_box_index()
        return jsonify(payload)

    # The route for specific box
    @app.route("/box/<box_id>")
    def return_box(box_id: str):
        payload = Box().return_box(box_id)
        return jsonify(payload)

    # The route for all vials
    @app.route("/vials")
    def return_all_vials():
        payload = Vial().return_all_vials()
        return jsonify(payload)

    # The route for vials of a specific box
    @app.route("/vials/<box_id>")
    def return_vials_box(box_id: str):
        payload = Vial().return_vials_box(box_id)
        return jsonify(payload)

    return app


def web(host="127.0.0.1", port=5000) -> None:
    app = create_app()
    app.run(host, port)
