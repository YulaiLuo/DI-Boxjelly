from flask_restful import Api
from .map_task import *
from .uil import *

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    # Create the API instance
    api = Api()

    api.add_resource(CreateUILResource, '/uil')
    api.add_resource(GetUILResource, '/uil/<uil_version>')
    api.add_resource(CreateUILGroupResource, '/uil/<uil_version>/groups')
    api.add_resource(CreateUILCategoryResource, '/uil/<uil_version>/categories')
    api.add_resource(MapTasksResource, '/uil/tasks')
    api.add_resource(MapTaskResource, '/uil/tasks/<task_id>')
    api.add_resource(MapTaskMetaResource, '/uil/tasks/<task_id>/meta')
    api.add_resource(DownloadMapTaskResource, '/uil/tasks/<task_id>/download')
    
    # Initialize the API
    api.init_app(app)
