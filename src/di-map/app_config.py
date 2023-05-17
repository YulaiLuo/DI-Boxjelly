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
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://boxjelly:di_boxjelly90082@101.43.110.249:27017/di?authSource=admin'
    
    # Medcat multiprocessing threshold
    # If the mapping is larger then MEDCAR_PROC_THRESHOLD - use multiprocessing
    # Otherwise - use the normal get_entities function
    MEDCAR_PROC_THRESHOLD  = 1000
    MEDCAT_NPROC = 2