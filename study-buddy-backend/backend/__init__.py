from flask import Flask
from backend.models import db
from backend.routes.routes import routes

def create_app():
    """Application factory for Study Buddy backend."""
    app = Flask(__name__)

    # DB config (SQLite by default)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flashcards.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Register routes
    app.register_blueprint(routes)

    return app
