from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
gravatar = Gravatar()
ckeditor = CKEditor()

manager = LoginManager()
manager.login_view = "authentication_pages.login"
manager.login_message = "You have to authorize first!"


def create_app():
    """Create flask application."""
    app = Flask(__name__)
    app.config.from_object("config.Config")

    bootstrap.init_app(app)
    gravatar.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app)
    manager.init_app(app)
    db.init_app(app)

    # Import parts of our application
    from .admin import admin_views
    from .authentication import authentication_views
    from .home import home_views
    from .posts import posts_views

    # Register Blueprints
    app.register_blueprint(admin_views.admin_functionality)
    app.register_blueprint(authentication_views.authentication_pages)
    app.register_blueprint(home_views.home_pages)
    app.register_blueprint(posts_views.posts_pages)

    return app
