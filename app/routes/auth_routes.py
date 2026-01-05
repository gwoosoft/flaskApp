from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.errors.errors import ValidationError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    """Register a new user (public endpoint) - role will default to 'user'"""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValidationError("JSON body must be an object")

    facade = current_app.config["user_facade"]
    user = facade.register_user(data)

    # Create access token for the newly registered user (identity must be a string)
    access_token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "status": "ok",
        "user": user,
        "access_token": access_token
    }), 201


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        raise ValidationError("JSON body must be an object")

    facade = current_app.config["user_facade"]
    user = facade.authenticate_user(data)

    # Create access token (identity must be a string)
    access_token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "status": "ok",
        "user": user,
        "access_token": access_token
    }), 200


@auth_bp.route("/auth/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Get the current authenticated user"""
    user_id = get_jwt_identity()  # Returns string, convert to int
    facade = current_app.config["user_facade"]
    user = facade.get_user(int(user_id))

    return jsonify({
        "status": "ok",
        "user": user
    }), 200

