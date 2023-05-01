from .bcrypt import init_bcrypt
from .db import init_db
from .jwt import init_jwt

_bcrypt = None
_mongo = None
_jwt = None

def init_utils(app):
    """
    Initialize the API, adding all the helpers to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    global _bcrypt, _mongo, _jwt

    # Initialize the Bcrypt
    _bcrypt = init_bcrypt(app)

    # Initialize the mongodb
    _mongo = init_db(app)

    # Initialize the JWTManager
    _jwt = init_jwt(app)

def get_mongo():
    if _mongo == None:
        raise Exception("MongoDB not initialized")
    return _mongo

def get_jwt():
    if _jwt is None:
        raise Exception("JWTManager not initialized")
    return _jwt

def get_bcrypt():
    if _bcrypt is None:
        raise Exception("Bcrypt not initialized")
    return _bcrypt
