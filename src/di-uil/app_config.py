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

    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://boxjelly:di_boxjelly90082@101.43.110.249:27017/di?authSource=admin'

