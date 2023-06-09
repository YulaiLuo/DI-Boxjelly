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
    