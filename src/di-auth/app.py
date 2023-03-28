"""
This module is responsible for user authentication and authorization.

The main function including: login, register, logout, and invite member.

Example:
    >>> from flask import Flask
    >>> from app_config import app_config
    >>> app = Flask(__name__)
    >>> app.run()
"""

from flask import Flask
from resources import api, mongo, bcrypt, mail, jwt

# Initialize the configuration of flask app
import app_config
app = Flask(__name__)
app.config.from_object(app_config)

api.init_app(app)
mongo.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
jwt.init_app(app)

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT= 8001
    DEBUG = True

    app.run(debug=DEBUG, host=HOST, port=PORT)