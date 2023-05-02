from flask import request, Response
from flask_restful import Resource
import requests

class NewUILCategoryResource(Resource):
   def post(self):
    # TODO: Creae a map task
    pass

class UpdateCategoryResource(Resource):
   def post(self):
      # TODO: Get detail of map task
      pass

class UILCategoryDetailResource(Resource):
   def get(self):
      # TODO: Get detail of map task
      pass

class DeleteUILCategoryResource(Resource):
   def delete(self):
      # TODO: Get detail of map task
      pass

class UILListResource(Resource):
   def get(self):
      # TODO: Get the uil list of a version
      pass
   