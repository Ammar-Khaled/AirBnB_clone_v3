#!/usr/bin/python3
""" View module for amenities endpoint """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city_id(city_id):
    """Return the list of all Place objects of a City by city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """Return a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_by_id(place_id):
    """Delete a Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create an Place object by city_id."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in attrs:
        abort(400, 'Missing user_id')

    user = storage.get(User, attrs['user_id'])
    if user is None:
        abort(404)

    if 'name' not in attrs:
        abort(400, 'Missing name')

    attrs['city_id'] = city_id
    place = Place(**attrs)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place_by_id(place_id):
    """Update an Place object by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    # get attributes from request body
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    for key, value in attrs.items():
        # if key is not a system attribute then update the field with key
        if key not in {'id', 'updated_at', 'created_at', 'user_id', 'city_id'}:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())
