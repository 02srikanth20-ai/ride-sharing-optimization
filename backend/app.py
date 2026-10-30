from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from engine import RideSharingSimulationEngine
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

engine = RideSharingSimulationEngine()

@app.route("/")
def def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/simulate", methods=["GET"])
def get_simulation():
    """Triggers a full platform simulation step and returns JSON metrics"""
    results = engine.run_full_simulation()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5000)