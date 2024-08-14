#!/usr/bin/python3
"""
creates states
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_show(state_id):
    """returns a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_update(state_id):
    """updates a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    exempt_keys = ['id', 'created_at', 'updated_at']
    for key, value in kwargs.items():
        if key not in exempt_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())


@app_views.route('/states', strict_slashes=False)
def states_list():
    """returns a list of all states"""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """deletes a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_create():
    """creates a new state"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201
