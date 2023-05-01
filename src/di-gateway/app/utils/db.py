from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """
    Initialize the MongoDB database

    Args:
        app (Flask): The Flask app
    """

    mongo.init_app(app, uri=app.config['MONGO_URI'])

