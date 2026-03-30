"""Application factory for the Bonnyrigg Pizza Blog."""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Database object shared across modules.
db = SQLAlchemy()

# Login manager handles secure user session loading.
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change-this-secret-key-before-production'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_blog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from . import models  # noqa: F401  # Registers database models.
    from .routes import register_routes

    register_routes(app)

    with app.app_context():
        db.create_all()
        models.seed_data()

    return app
