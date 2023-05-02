from .cors import init_cors
from .db import init_db
from .jwt import init_jwt

def init_utils(app):
    """
    Initialize the API, adding all the helpers to the Flask app.

    Args:
        app (Flask): The Flask app
    """

    # Initialize the mongodb
    init_db(app)


