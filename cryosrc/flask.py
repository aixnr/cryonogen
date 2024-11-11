from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

from .manifest import Manifest


def create_app(db: str) -> Flask:
    # Initialize the app
    app = Flask(__name__)
    app.debug = False
    CORS(app)

    with sqlite3.connect(db) as conn:
        manifest = Manifest(conn=conn)

    conn.close()

    @app.route("/boxes")
    def return_all_boxes():
        payload = manifest.return_box_index()
        return jsonify(payload)

    @app.route("/box/<box_id>")
    def return_box(box_id: str):
        payload = manifest.return_box(box_id)
        return jsonify(payload)

    # The route for all vials
    @app.route("/vials")
    def return_all_vials():
        payload = manifest.return_all_vials()
        return jsonify(payload)

    # The route for vials of a specific box
    @app.route("/vials/<box_id>")
    def return_vials_box(box_id: str):
        payload = manifest.return_vials_box(box_id)
        return jsonify(payload)

    return app


def web(db: str, host="127.0.0.1", port=5000) -> None:
    app = create_app(db=db)
    app.run(host, port)
