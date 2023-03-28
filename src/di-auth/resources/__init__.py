from flask_restful import Api
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from .invite import Invite
from .register import Register
from .login import Login
from .logout import Logout

# Helper instances
api = Api()
mongo = PyMongo()
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()

# Add route
api.add_resource(Register, '/di_auth/register',resource_class_args=(mongo, bcrypt))
api.add_resource(Invite, '/di_auth/invite/<string:access_token>',resource_class_args=(mongo, mail))
api.add_resource(Login, '/di_auth/login', resource_class_args=(mongo, bcrypt,))
api.add_resource(Logout, '/di_auth/logout', resource_class_args=(mongo, mail))
