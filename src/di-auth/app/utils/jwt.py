from flask_jwt_extended import JWTManager

def init_jwt(app):
    """
    Initialize the JWTManager

    Args:
        app (Flask): The Flask app
    """

    jwt = JWTManager(app)

    return jwt