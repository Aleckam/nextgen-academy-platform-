from .auth import bp as auth_bp
from .users import bp as users_bp
from .schools import bp as schools_bp
from .classes import bp as classes_bp
from .content import bp as content_bp
from .certificates import bp as certificates_bp
from .subscriptions import bp as subscriptions_bp
from .blog import bp as blog_bp
from .admin import bp as admin_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(schools_bp, url_prefix="/api/schools")
    app.register_blueprint(classes_bp, url_prefix="/api/classes")
    app.register_blueprint(content_bp, url_prefix="/api/content")
    app.register_blueprint(certificates_bp, url_prefix="/api/certificates")
    app.register_blueprint(subscriptions_bp, url_prefix="/api/subscriptions")
    app.register_blueprint(blog_bp, url_prefix="/api/blog")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
