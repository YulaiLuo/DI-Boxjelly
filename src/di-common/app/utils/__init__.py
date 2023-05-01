# from .sendgrid import init_sendgrid
from .db import init_db

_bcrypt = None
_mongo = None

def init_utils(app):
    """
    Initialize the API, adding all the helpers to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    global _bcrypt, _mongo

    # Initialize the Bcrypt
    # _bcrypt = init_bcrypt(app)

    # Initialize the mongodb
    _mongo = init_db(app)

def get_mongo():
    if _mongo == None:
        raise Exception("MongoDB not initialized")
    return _mongo

