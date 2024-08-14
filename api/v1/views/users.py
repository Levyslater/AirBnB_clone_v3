#!/usr/bin/python3
"""
creates users
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def users_list():
    """returns a list of all users"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', strict_slashes=False)
def users_show(user_id):
    """returns a user object"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def users_delete(user_id):
    """deletes a user"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_create():
    """creates a new user"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'email' not in kwargs:
        return abort(400, 'Missing email')
    if 'password' not in kwargs:
        return abort(400, 'Missing password')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def users_update(user_id):
    """updates a user"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    exempt_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in kwargs.items():
        if key not in exempt_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
