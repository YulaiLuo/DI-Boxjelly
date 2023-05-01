from flask import Flask
from .api import init_api
from .utils import init_utils

def create_app():
    """
    Initialize the Flask app

    Example:
        from app import create_app
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    """

    # Initialize the configuration of flask app
    app = Flask(__name__)
    app.config.from_object('app_config.Config')
    
    # Initialize all the helpers to the Flask app
    with app.app_context():
        init_api(app)
        init_utils(app)

    return app