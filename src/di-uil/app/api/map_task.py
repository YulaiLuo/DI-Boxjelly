from flask import request, Response
from flask_restful import Resource
import requests
from marshmallow import Schema, fields, ValidationError, validate

class MapTaskSchema(Schema):

    # TODO:
    pass


class NewMapTaskResource(Resource):
   def post(self):
    # TODO: Creae a map task
    # Main function to do mapping
    pass

class MapTaskDetailResource(Resource):
   def get(self):
      # TODO: Get detail of map task
      pass

class DeleteMapTaskResource(Resource):
   def post(self):
      # TODO: Get detail of map task
      pass

