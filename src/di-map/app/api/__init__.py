from flask_restful import Api
from .medcat import Translate

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """

    # Create the API instance
    api = Api()

    # Add route
    api.add_resource(Translate, '/map/translate')

    # Initialize the API
    api.init_app(app)



