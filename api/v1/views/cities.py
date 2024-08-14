#!/usr/bin/python3
"""
creates cities
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_list_by_state(state_id):
    """returns a list of cities in a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False)
def city_show(city_id):
    """returns a city object"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_delete(city_id):
    """deletes a city"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_create(state_id):
    """creates a new city in a state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return abort(400, 'Missing name')
    kwargs['state_id'] = state_id

    city = City(**kwargs)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_update(city_id):
    """updates a city"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    exempt_keys = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in kwargs.items():
        if key not in exempt_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
