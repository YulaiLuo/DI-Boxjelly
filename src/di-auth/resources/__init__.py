from flask_restful import Api
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from .invite import Invite
from .register import EmailRegister
from .login import EmailLogin
from .logout import Logout

# Helper instances
api = Api()
mongo = PyMongo()
bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()

# Add route
api.add_resource(EmailRegister, '/di_auth/register/email',resource_class_args=(mongo, bcrypt))
api.add_resource(Invite, '/di_auth/invite/<string:access_token>',resource_class_args=(mongo, mail))
api.add_resource(EmailLogin, '/di_auth/login/email', resource_class_args=(mongo, bcrypt,))
api.add_resource(Logout, '/di_auth/logout', resource_class_args=(mongo, mail))
