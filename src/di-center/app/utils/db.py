import mongoengine as mongo

def init_db(app):
    mongo.connect(host=app.config['MONGO_URI'])

