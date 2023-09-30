#!/usr/bin/python3
""" View module for places reviews endpoint """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place_id(place_id):
    """Return the list of all Review objects of a Place by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """Return a Review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_by_id(review_id):
    """Delete a Review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create an Review object by place_id."""
    review = storage.get(Place, place_id)
    if review is None:
        abort(404)

    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in attrs:
        abort(400, 'Missing user_id')

    user = storage.get(User, attrs['user_id'])
    if user is None:
        abort(404)

    if 'text' not in attrs:
        abort(400, 'Missing text')

    attrs['place_id'] = place_id
    review = Review(**attrs)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review_by_id(review_id):
    """Update an Review object by its id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    # get attributes from request body
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    for key, value in attrs.items():
        # if key is not a system attribute then update the field with key
        if key not in {'id', 'updated_at', 'created_at', 'user_id',
                       'place_id'}:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict())
