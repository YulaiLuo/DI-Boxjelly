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

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://boxjelly:di_boxjelly90082@mongo:27017/di?authSource=admin'

    # JWT Setting
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False   # Only set flask in development environment
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'di'
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or timedelta(minutes=60)    
    JWT_CSRF_CHECK_FORM = True

    # Avatar settings
    AVATAR_FOLDER = '~/data/di-data/di-auth/avatars'
