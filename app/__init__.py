from flask import Flask
from flask_cors import CORS
from .config import Config
from .handlers import init_oauth
import logging

def create_app():
    app = Flask(__name__)
    # Set timeouts at the root level
    app.config['TIMEOUT'] = 540 
    # Enable CORS for all routes
    CORS(app, supports_credentials=True)
    
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
