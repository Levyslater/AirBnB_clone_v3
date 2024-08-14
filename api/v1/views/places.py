#!/usr/bin/python3
"""
Create a new view for Place objects that handles all
default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def list_all_places_in_a_city(city_id):
    """returns a list of all places in a city"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def show_place_by_id(place_id):
    """returns a place object by its id"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """creates a new place"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        return abort(400, 'Missing user_id')
    if 'name' not in kwargs:
        return abort(400, 'Missing name')
    user = storage.get(User, kwargs['user_id'])
    if user is None:
        return abort(404)

    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    exempt_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in kwargs.items():
        if key not in exempt_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
