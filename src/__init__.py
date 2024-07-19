from src.config import Config

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config: Config = None) -> Flask:
    """Factory to create the Flask application
    :return: A `Flask` application instance
    """

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    if test_config:
        app.config.from_object(test_config)

    with app.app_context():
        db.create_all()

        _register_blueprints(app)

        CORS(app)

    return app


def _register_blueprints(app: Flask) -> None:
    from src.index.views import index_bp
    app.register_blueprint(index_bp)
