#!/usr/bin/python3
"""
Creates a new flask app
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns a JSON error message for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
