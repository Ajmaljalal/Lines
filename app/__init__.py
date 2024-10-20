from flask import Flask
from .config import Config
from .handlers import init_oauth
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    init_oauth(app)

    try:
        from .routes import main
        app.register_blueprint(main)
    except ImportError as e:
        app.logger.error(f"Error importing routes: {e}")
        raise

    return app
