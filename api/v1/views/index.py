#!/usr/bin/python3
"""
creates flask app (app_views)
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_api():
    """returns a JSON status"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def stats_api():
    """"
    return count of each db storage modules
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
