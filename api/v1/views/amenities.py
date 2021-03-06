#!/usr/bin/python3
"""Endpoints related to States"""

from flask import jsonify, abort, request
from . import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'])
def amenities():
    """ Route for getting Amenity data. """
    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            return 'Not a JSON', 400
        if 'name' not in json:
            return 'Missing name', 400
        amenity = Amenity(**json)
        storage.new(amenity)
        storage.save()
        return amenity.to_dict(), 201

    return jsonify([amenity.to_dict() for amenity
                    in storage.all('amenity').values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id):
    """ Route for getting specific state data. """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return '{}', 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            return 'Not a JSON', 400
        for k, v in json.items():
            if k in ('id', 'updated_at', 'created_at'):
                continue
            setattr(amenity, k, v)
        amenity.save()
        return jsonify(amenity.to_dict()), 200

    return jsonify(amenity.to_dict())
