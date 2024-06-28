#!/usr/bin/env python3
"""
api application
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins":"*"}})

@app.errorhandler(404)
def not_found(error):
    res = make_response(jsonify({"error": "Not found"}), 404)
    return res

if __name__ == "__main__":
    host = environ.get("API_HOST", "0.0.0.0")
    port = environ.get("API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
