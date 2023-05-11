from flask_restful import Api
from .map_task.map_task import *
from .map_task.map_task_download import *
from .map_task.map_task_item import *
from .map_task.map_task_board import *
from .map_task.map_task_meta import *

from .code.system import *
from .code.concept import *
from .code.group import *

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    
    # Create the API instance
    api = Api()

    api.add_resource(CodeSystemResource, '/uil')
    api.add_resource(ConceptGroupResource, '/uil/groups')
    api.add_resource(ConceptResource, '/uil/concepts')

    api.add_resource(MapTaskBoardResource, '/uil/board')
    api.add_resource(MapTaskResource, '/uil/task')
    api.add_resource(MapTaskMetaResource, '/uil/task/meta')

    api.add_resource(MapTaskItemResource, '/uil/task/<task_id>/<index>')
    api.add_resource(DownloadMapTaskResource, '/uil/task/<task_id>/download')
    
    # Initialize the API
    api.init_app(app)
