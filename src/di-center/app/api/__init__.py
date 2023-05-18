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

from .dashboard.dashboard import *

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """

    # Create the API instance
    api = Api()

    api.add_resource(CodeSystemResource, '/center')
    api.add_resource(ConceptGroupResource, '/center/groups')
    api.add_resource(ConceptResource, '/center/concepts')
    api.add_resource(AllConceptResource, '/center/concepts/all')

    api.add_resource(MapTaskBoardsResource, '/center/boards')
    api.add_resource(MapTaskResource, '/center/boards/tasks')

    api.add_resource(MapTaskDetailResource, '/center/boards/task/detail')
    api.add_resource(MapTaskMetaResource, '/center/boards/task/meta')
    api.add_resource(DownloadMapTaskResource, '/center/boards/task/download')
    api.add_resource(MapTaskCurateResource, '/center/boards/task/curate')

    api.add_resource(TopLeftResource, '/center/dashboard/top-left')
    api.add_resource(TopMiddleResource, '/center/dashboard/top-middle')
    api.add_resource(TopRightResource, '/center/dashboard/top-right')
    api.add_resource(HelloResource, '/center/dashboard/hello')


    # Initialize the API
    api.init_app(app)
