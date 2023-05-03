import mongoengine as mongo
# from flask_pymongo import PyMongo

# db = PyMongo()

def init_db(app):
    mongo.connect(host=app.config['MONGO_URI'])
    # db.init_app(app, uri=app.config['MONGO_URI'])

