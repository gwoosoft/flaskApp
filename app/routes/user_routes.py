from flask import Blueprint, jsonify, request, current_app

from app.errors.errors import ValidationError

user_bp = Blueprint("users", __name__)

@user_bp.route("/users", methods=["POST"])
def create_user():
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
def get_user(user_id):
    facade = current_app.config["user_facade"]
    user = facade.get_user(user_id)

    return jsonify({
        "status": "ok",
        "user": user
    }), 200
