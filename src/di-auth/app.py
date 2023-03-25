from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_mail import Mail
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity,
from flask_jwt_extended import get_jwt
# from marshmallow import Schema, fields, ValidationError
from resources.regitser import Register
from resources.login import Login
from resources.logout import Logout
from resources.invite import Invite


app = Flask(__name__)

# Flask-Mail configuration
mail_settings = {
    "MAIL_SERVER": 'smtp.sendgrid.net',
    "MAIL_PORT": 465,
    # "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "apikey",
    "MAIL_PASSWORD": "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"
    # "MAIL_USERNAME": os.environ['EMAIL_USER'],
    # "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
db_settings = {
    "MONGO_URI":'mongodb://boxjelly:di_boxjelly90082@101.43.110.249:27017/di?authSource=admin',
}
jwt_settings = {
    'JWT_TOKEN_LOCATION': ['cookies'],
    "JWT_SECRET_KEY":"di",
    "JWT_ALGORITHM":"HS256",
    'JWT_ACCESS_TOKEN_EXPIRES':3600,
}


# Initialize
app.config.update(mail_settings)
app.config.update(db_settings)
app.config.update(jwt_settings)

# Initialize
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
api = Api(app)
mail = Mail(app)
jwt = JWTManager(app)

# Add route
api.add_resource(Register, '/di_auth/register',resource_class_args=(mongo, bcrypt))
api.add_resource(Invite, '/di_auth/invite/<string:access_token>',resource_class_args=(mongo, mail))
api.add_resource(Login, '/di_auth/login', resource_class_args=(mongo, bcrypt,))
api.add_resource(Logout, '/di_auth/logout', resource_class_args=(mongo, mail))

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT= 81
    DEBUG = True

    app.run(debug=DEBUG, host=HOST, port=PORT)