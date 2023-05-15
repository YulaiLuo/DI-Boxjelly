from flask_restful import Api
from .task.task import *
from .task.task_download import *
from .task.task_curate import *
from .task.task_board import *
from .task.task_meta import *
from .task.task_detail import *

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
    api.add_resource(AllConceptResource, '/uil/concepts/all')

    api.add_resource(MapTaskBoardsResource, '/uil/boards')
    api.add_resource(MapTaskResource, '/uil/boards/tasks')
    api.add_resource(MapTaskDetailResource, '/uil/boards/task/detail')
    api.add_resource(MapTaskMetaResource, '/uil/boards/task/meta')

    api.add_resource(MapTaskCurateResource, '/uil/task/<task_id>/<index>')
    api.add_resource(DownloadMapTaskResource, '/uil/boards/task/download')
    
    # Initialize the API
    api.init_app(app)
