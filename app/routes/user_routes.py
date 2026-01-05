from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required
from app.utils.auth_utils import admin_required
from app.errors.errors import ValidationError

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
@jwt_required()
@admin_required
def create_user():
    """Create a new user (admin only)"""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValidationError("JSON body must be an object")

    facade = current_app.config["user_facade"]
    user = facade.create_user(data)

    return jsonify({
        "status": "ok",
        "user": user
    }), 201


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    """Get a specific user by ID (requires authentication)"""
    facade = current_app.config["user_facade"]
    user = facade.get_user(user_id)

    return jsonify({
        "status": "ok",
        "user": user
    }), 200
