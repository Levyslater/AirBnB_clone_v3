#!/usr/bin/python3
"""
This module creates a Flask application and registers the API blueprint.
It also sets up CORS, handles teardown, and customizes error responses.
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes under /api/v1/*
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

# Register the API blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown of the Flask app context."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 error response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    # Get the host and port from environment
    # variables or default to '0.0.0.0' and 5000
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', 5000)

    # Run the Flask app with threading and debug mode enabled
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
