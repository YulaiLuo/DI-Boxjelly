from flask import request, Response
from flask_restful import Resource
import requests
from marshmallow import Schema, fields, ValidationError, validate



class CurateMappedUILCategory(Resource):
   def get(self):
      # TODO: change the mapped UIL category
      pass

class MappedItemDetailResource(Resource):
    def get(self):
        # TODO: get the detail of a mapped item
