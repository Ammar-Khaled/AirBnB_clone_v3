#!/usr/bin/python3
"""
Web server
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(_):
    """Close the storage session."""
    storage.close()


@app.errorhandler(404)
def not_found(_):
    """Handle the 404 not found error."""
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST') or '0.0.0.0'
    HBNB_API_PORT = getenv('HBNB_API_PORT') or '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
