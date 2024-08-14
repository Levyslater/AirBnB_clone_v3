#!/usr/bin/python3
"""
This module creates views for State objects and handles all default RESTful API actions.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_list():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_show(state_id):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_delete(state_id):
    """Deletes a State object: DELETE /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """Creates a new State: POST /api/v1/states"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    exempt_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in exempt_keys:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200

