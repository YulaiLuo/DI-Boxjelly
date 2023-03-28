"""
This file is used to store all the configuration variables for the flask app.

Including mail server, database, JWT secret key, etc.

Example:
    >>> from flask import Flask
    >>> from app_config import app_config
    >>> app = Flask(__name__)
    >>> app.config.from_object(app_config)
"""

# Mail Setting
MAIL_SERVER = 'smtp.sendgrid.net'
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USERNAME = "apikey"
MAIL_PASSWORD = "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"

# MAIL_USE_SSL = True
# MAIL_USERNAME = os.environ['EMAIL_USER'],
# MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

# Database Setting
MONGO_URI = 'mongodb://boxjelly:di_boxjelly90082@101.43.110.249:27017/di?authSource=admin'

# JWT Setting
JWT_TOKEN_LOCATION = ['cookies']
JWT_SECRET_KEY = "di"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRES = 3600

