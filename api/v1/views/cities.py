#!/usr/bin/python3
""" View module for cities endpoint """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state_route(state_id):
    """Return the list of all City objects of a State by state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Return a City object by city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_by_id(city_id):
    """Delete a City object by city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city_by_state_id(state_id):
    """Create a City object by state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    attrs['state_id'] = state_id
    req_attrs = City.getRequiredAttributes()
    for attr in req_attrs:
        if attr not in attrs:
            abort(400, 'Missing {}'.format(attr))

    city = City(**attrs)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city_by_id(city_id):
    """Update a City object by city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    # get attributes from request body
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    for key, value in attrs.items():
        # if key is not a system attribute then update the field with key
        if key not in {'id', 'updated_at', 'created_at', 'state_id'}:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
