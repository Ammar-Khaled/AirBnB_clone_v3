#!/usr/bin/python3
""" View module for users endpoint """

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Return a list of all User objects"""
    users = storage.all(User) or {}
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Return a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    """Delete a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create an User object."""
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    for field in {'email', 'password'}:
        if field not in attrs:
            abort(400, 'Missing {}'.format(field))

    user = User(**attrs)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    """Update an User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    # get attributes from request body
    attrs = request.get_json(silent=True)
    if attrs is None:
        abort(400, 'Not a JSON')

    for key, value in attrs.items():
        # if key is not a system attribute then update the field with key
        if key not in {'id', 'updated_at', 'created_at', 'email'}:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict())
