#!/usr/bin/python3
""" View module for places endpoint """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


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


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """Search for places."""
    lists = request.get_json()
    if lists is None:
        abort(400, 'Not a JSON')

    try:
        states = lists['states']  # list of state ids
    except Exception:
        states = []
    try:
        cities = lists['cities']  # list of city ids
    except Exception:
        cities = []
    try:
        amenities = lists['amenities']  # list of amenity ids
    except Exception:
        amenities = []

    if len(lists) == 0 or (len(states) == 0 and len(cities) == 0 and len(amenities) == 0):
        return jsonify([p.to_dict() for p in storage.all(Place).values()])

    cities_to_search = set()
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                cities_to_search.add(city.id)
    for city_id in cities:
        cities_to_search.add(city_id)

    places = set()
    all_places = storage.all(Place).values()
    for place in all_places:
        print(f"place: {place}")
        if place.city_id in cities_to_search:
            print(f"place.city_id: {place.city_id}")
            places.add(place)

    if amenities:
        for amenity in amenities:
            for place in places:
                if amenity not in place.amenities:
                    places.pop(place)

    return jsonify([p.to_dict() for p in places])
