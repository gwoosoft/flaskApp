from flask import Flask, jsonify
from werkzeug.exceptions import BadRequest
from app.errors.errors import AppError
from dotenv import load_dotenv
from app.extensions import db, jwt
from app.config import Config
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.routes.user_routes import user_bp
from app.routes.auth_routes import auth_bp
from app.facades.user_facade import UserFacade

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # ---- global error handlers ----
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    user_repo = UserRepository()
    user_service = UserService(user_repo)
    user_facade = UserFacade(user_service)

    app.config["user_facade"] = user_facade

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return "Hello, World!"

    @app.route("/routes")
    def routes():
        return str(app.url_map)

    return app


def register_error_handlers(app):

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        # malformed JSON or bad request payload
         return jsonify({"error": "Malformed JSON body", "code": "validation_error"}), 400

    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        payload = {
            "error": e.message,
            "code": e.code,
            **getattr(e, "details", {})
        }

        return jsonify(payload), e.status_code