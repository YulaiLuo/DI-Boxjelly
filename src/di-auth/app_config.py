"""
This file is used to store all the configuration variables for the flask app.

Including mail server, database, JWT secret key, etc.

Example:
    >>> from flask import Flask
    >>> from app_config import app_config
    >>> app = Flask(__name__)
    
"""

import os 
from datetime import timedelta

class Config:

    # Mail Setting
    # MAIL_SERVER = 'smtp.sendgrid.net'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = "apikey"
    # MAIL_PASSWORD = "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"

    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ['EMAIL_USER'],
    # MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://boxjelly:di_boxjelly90082@101.43.110.249:27017/di?authSource=admin'

    # JWT Setting
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False   # Only set flask in development environment
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'di'
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or timedelta(minutes=1)    
    JWT_CSRF_CHECK_FORM = True
    # JWT_COOKIE_SAMESITE = "Lax"

    # Avatar settings
    AVATAR_FOLDER = os.path.join(os.getcwd(),'data','avatars')