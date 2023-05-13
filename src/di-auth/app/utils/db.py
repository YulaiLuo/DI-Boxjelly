from flask_pymongo import PyMongo
import mongoengine as mongo


def init_db(app):
    """
    Initialize the MongoDB database

    Args:
        app (Flask): The Flask app
    """
    mongo.connect(host=app.config['MONGO_URI'])

    pymongo = PyMongo(app, uri=app.config['MONGO_URI'])
    return pymongo
