from flask_restful import Api

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    # Create the API instance
    api = Api()

    # TODO: Add resource to path

    # Initialize the API
    api.init_app(app)
