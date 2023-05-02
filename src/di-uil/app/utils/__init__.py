from .db import init_db

def init_utils(app):
    """
    Initialize the API, adding all the helpers to the Flask app.

    Args:
        app (Flask): The Flask app
    """

    # Initialize the mongodb
    init_db(app)


