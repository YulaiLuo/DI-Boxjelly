from flask_restful import Api
from .register import EmailRegister
from .login import EmailLogin
from .logout import Logout
from ..utils import get_mongo, get_bcrypt, get_jwt

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    # Create the API instance
    api = Api()

    # Get the helper instances
    mongo = get_mongo()
    bcrypt = get_bcrypt()
    jwt = get_jwt()

    # Add route
    api.add_resource(EmailRegister, '/auth/register/email',resource_class_args=(mongo, bcrypt,))
    
    # api.add_resource(Invite, '/auth/invite',resource_class_args=(mongo, mail))
    api.add_resource(EmailLogin, '/auth/login/email',resource_class_args=(mongo, bcrypt,))
    api.add_resource(Logout, '/auth/logout', resource_class_args=(mongo, jwt,))

    # Initialize the API
    api.init_app(app)
