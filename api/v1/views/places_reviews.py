#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def show_reviews_of_place(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def show_review_by_id(review_id):
    """
    Retrieves a Review object by its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object for a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    user_id = kwargs.get('user_id')
    if user_id is None:
        return abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    text = kwargs.get('text')
    if text is None:
        return abort(400, 'Missing text')
    review = Review(**kwargs)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object by its id
    """
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)

    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')

    kwargs = request.get_json()
    if not kwargs:
        return abort(400, 'Not a JSON')

    # Ignored keys
    ignored_keys = {'id', 'user_id', 'place_id', 'created_at', 'updated_at'}

    for key, value in kwargs.items():
        if key not in ignored_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
