import os
from datetime import timedelta


class Config:
    """
    This class is used to store all the configuration variables for the flask app.

    Example:
        >>> from flask import Flask
        >>> import app_config
        >>> app = Flask(__name__)
        >>> app.config.from_object('app_config.Config')

    """

    # JWT Setting
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'di'
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_CSRF_CHECK_FORM = True
    # JWT_COOKIE_SAMESITE = "Lax"

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://boxjelly:di_boxjelly90082@mongo:27017/di?authSource=admin'

    # Microservice Map
    # SERVICE_MAP = {
    #     "auth": "http://localhost:8001/auth",
    #     "center": "http://localhost:8002/center",
    #     "map": "http://localhost:8003/map"
    # }
    SERVICE_MAP = {
        "auth": "http://di-auth:8001/auth",
        "center": "http://di-center:8002/center",
        "map": "http://di-map:8003/map"
    }
