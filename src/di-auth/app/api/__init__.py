from flask_restful import Api
from .login import EmailLogin
from .logout import Logout
from ..utils import get_mongo, get_bcrypt, get_jwt
from .team import TeamResource
from .user import UserResource
from .avatar import AvatarResource
from .invite import InviteResource, AcceptInviteResource


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

    # Team resource
    api.add_resource(TeamResource, '/auth/team')

    # User resource
    api.add_resource(UserResource, '/auth/user')
    api.add_resource(AvatarResource, '/auth/user/avatar')

    # Invite resource
    api.add_resource(InviteResource, '/auth/team/invite')
    api.add_resource(AcceptInviteResource, '/auth/team/accept',
                     resource_class_args=(bcrypt,))

    api.add_resource(EmailLogin, '/auth/login/email',
                     resource_class_args=(mongo, bcrypt,))
    api.add_resource(Logout, '/auth/logout', resource_class_args=(mongo, jwt,))

    # Initialize the API
    api.init_app(app)
