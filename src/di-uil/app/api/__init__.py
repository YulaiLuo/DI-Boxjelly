from flask_restful import Api
from .map_task import CreateMapTaskResource, MapTaskDetailResource, DeleteMapTaskResource

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    # Create the API instance
    api = Api()

    # TODO: Add resource to path
    api.add_resource(CreateMapTaskResource, '/uil/tasks')

    # Initialize the API
    api.init_app(app)
