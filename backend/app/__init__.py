from flask import Flask, jsonify

from app.config import Config
from app.extensions import db, migrate, jwt, cors


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    from app import models  # noqa: F401  ensures models are registered before migrations

    from app.api import register_blueprints

    register_blueprints(app)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "nextgen-academy-backend"})

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not_found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        app.logger.exception(e)
        return jsonify({"error": "internal_server_error"}), 500

    return app
