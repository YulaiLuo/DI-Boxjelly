from flask_restful import Api
from flask_pymongo import PyMongo
from .ontoserver import Translate

# Helper instances
api = Api()
mongo = PyMongo()

# Add route
api.add_resource(Translate, '/map/ontoserver/translate')
