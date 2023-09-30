#!/usr/bin/python3
""" View module for amenities endpoint """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Return a list of all Amenity objects"""
    amenities = storage.all(Amenity) or {}
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_by_id(amenity_id):
    """Return a Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_by_id(amenity_id):
    """Delete a Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Create an Amenity object."""
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')
    if 'name' not in attrs:
        abort(400, 'Missing name')

    amenity = Amenity(**attrs)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity_by_id(amenity_id):
    """Update an Amenity object by amenity_id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    # get attributes from request body
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    for key, value in attrs.items():
        # if key is not a system attribute then update the field with key
        if key not in {'id', 'updated_at', 'created_at'}:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict())
