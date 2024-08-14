#!/usr/bin/python3
"""
creates Amenities
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities_list():
    """returns a list of all amenities"""
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_show(amenity_id):
    """returns an amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id):
    """deletes an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_create():
    """creates a new amenity"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return abort(400, 'Missing name')

    amenity = Amenity(**kwargs)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenities_update(amenity_id):
    """updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    exempt_keys = ['id', 'created_at', 'updated_at']
    for key, value in kwargs.items():
        if key not in exempt_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
