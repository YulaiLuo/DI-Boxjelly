from flask_pymongo import PyMongo


def init_db(app):
    """
    Initialize the MongoDB database

    Args:
        app (Flask): The Flask app
    """
    mongo = PyMongo(app, uri=app.config['MONGO_URI'])
    return mongo
