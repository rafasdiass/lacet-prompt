# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request, jsonify

from app_balance.extensions import db
from app_balance.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/', methods=['GET'])
def get_users():
    """Get all users."""
    users = User.query.all()
    return jsonify([user.username for user in users]), 200


@blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a single user by ID."""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'is_admin': user.is_admin,
        'active': user.active,
    }), 200


@blueprint.route('/', methods=['POST'])
def create_user():
    """Create a new user."""
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User(username=username, email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created', 'id': user.id}), 201


@blueprint.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user."""
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = data['password']

    db.session.commit()
    return jsonify({'message': 'User updated'}), 200


@blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 204
