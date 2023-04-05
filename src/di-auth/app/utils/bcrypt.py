from flask_bcrypt import Bcrypt


def init_bcrypt(app):
    """
    Initialize the Bcrypt which is used to hash passwords

    Args:
        app (Flask): The Flask app
    """

    bcrypt = Bcrypt(app)

    return bcrypt