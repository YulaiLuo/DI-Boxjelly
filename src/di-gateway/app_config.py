import os

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
    JWT_TOKEN_LOCATION = os.environ.get('JWT_TOKEN_LOCATION') or ['cookies']
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'di'
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM') or 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES') or 3600

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://boxjelly:di_boxjelly90082@101.43.110.249:27017/di?authSource=admin'

    # Microservice Map
    SERVICE_MAP = {
        "auth": "http://di-auth:8001/auth",
        "map": "http://di-map:8003/map"
    }
    # SERVICE_MAP = {
    #     "auth": "http://localhost:8001/auth",
    #     "map": "http://localhost:8003/map"
    # }