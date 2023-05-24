from flask_restful import Api
from .task.task import *
from .task.task_download import *
from .task.task_curate import *
from .task.task_board import *
from .task.task_meta import *
from .task.task_detail import *

from .codesystem.system import *
from .codesystem.download import *
from .codesystem.group import *
from .codesystem.version import *

from .dashboard.dashboard import *

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """

    # Create the API instance
    api = Api()

    api.add_resource(CodeSystemResource, '/center/codesystem')
    api.add_resource(CodeSystemVersionResource, '/center/codesystem/versions')
    api.add_resource(ConceptGroupResource, '/center/codesystem/groups')
    api.add_resource(DownloadCodeSystemResource, '/center/codesystem/download/<version>')

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
    api.add_resource(MapItemStatusRatioResource, '/center/dashboard/item-status-ratio')
    api.add_resource(PredictSingleResource, '/center/dashboard/predict')

    # Initialize the API
    api.init_app(app)
