from flask import Blueprint
from flask_restful import Api
from .auth import UserEmailLoginResource
from .gateway import GatewayResource 


def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    # Create the API instance
    api = Api()

    # Auth service routes
    api.add_resource(UserEmailLoginResource, '/auth/login/email')

    # All other routes are forwarded to the appropriate service
    api.add_resource(GatewayResource, '/<path:path>')

    # Initialize the API
    api.init_app(app)
