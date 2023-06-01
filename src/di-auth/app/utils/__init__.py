from .bcrypt import init_bcrypt
from .db import init_db
from .jwt import init_jwt
from app.models import User, Team, UserTeam

_bcrypt = None
_mongo = None
_jwt = None

def init_utils(app):
    """
    Initialize the API, adding all the helpers to the Flask app.

    Args:
        app (Flask): The Flask app
    """
    global _bcrypt, _mongo, _jwt

    # Initialize the Bcrypt
    _bcrypt = init_bcrypt(app)

    # Initialize the mongodb
    _mongo = init_db(app)

    # Initialize the JWTManager
    _jwt = init_jwt(app)

    # Initialize the first user
    if Team.objects().count() == 0:
        print("No user found, creating default user")
        team = Team(name='Research team')
        user = User(username='admin',
                    email='diboxjelly@student.unimelb.edu.au',
                    password=_bcrypt.generate_password_hash('diboxjelly').decode('utf-8'),
                    first_name='Admin',
                    last_name='Admin',
                    gender='Other')
        user_team = UserTeam(user_id=user,
                 team_id=team,
                 role='owner',
                 invite_by=user,
                 status='active')
        team.save()
        user.save()
        user_team.save()

def get_mongo():
    if _mongo == None:
        raise Exception("MongoDB not initialized")
    return _mongo

def get_jwt():
    if _jwt is None:
        raise Exception("JWTManager not initialized")
    return _jwt

def get_bcrypt():
    if _bcrypt is None:
        raise Exception("Bcrypt not initialized")
    return _bcrypt
