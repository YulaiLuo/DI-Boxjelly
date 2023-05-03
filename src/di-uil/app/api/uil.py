from flask import request, jsonify
from flask_restful import Resource
from ..models import UILCategory, UIL, UILGroup
from ..schemas import CreateUILCategoryInputSchema, CreateUILInputSchema, CreateUILGroupInputSchema
import requests
from marshmallow import ValidationError
from collections import Counter
from bson import ObjectId

class CreateUILCategoryResource(Resource):
   def post(self, uil_version):
      # TODO: Creae a category resource
      
      schema = CreateUILCategoryInputSchema()

      try:
         new_uil_category_data = schema.load(request.form)

         uil = UIL.objects(version=uil_version).first()
         if not uil:
            response = jsonify(code=404, err="UIL_NOT_FOUND")
            response.status_code = 404
            return response

         # convert id string to object id
         new_uil_category_data['uil_id'] = uil.id
         new_uil_category_data['create_by'] = ObjectId(new_uil_category_data['create_by'])
         # new_uil_category_data['group_id'] = ObjectId(new_uil_category_data['group_id'])

         # create uil and save
         new_uil_category = UILCategory(**new_uil_category_data)
         new_uil_category.save()

         response = jsonify(code=200,msg="ok", data={'id': str(new_uil_category.id)})
         response.status_code = 200
         return response
   
      except ValidationError as err:
         print(err)
         response = jsonify(code=400, err="INVALID_INPUT")
         response.status_code = 400
         return response
      
      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response

class CreateUILResource(Resource):

   def post(self):
      # Create schema new uil API input schema
      schema = CreateUILInputSchema()

      try:
         # load the data
         new_uil_data = schema.load(request.form)

         # convert id string to object id
         new_uil_data['create_by'] = ObjectId(new_uil_data['create_by'])

         # create uil and save
         new_uil = UIL(**new_uil_data)
         new_uil.save()

         response = jsonify(code=200,msg="ok", data={'version': new_uil.version})
         response.status_code=200
         return response

      except ValidationError as err:
         print(err)
         response = jsonify(code=400, err="INVALID_INPUT")
         response.status_code = 400
         return response
      # TODO: duplicate key exception
      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response

class CreateUILGroupResource(Resource):      

   def post(self, uil_version):
      # Create schema new map task API input schema
      schema = CreateUILGroupInputSchema()

      try:
         # load the data
         new_uil_group_data = schema.load(request.form)

         # convert id string to object id
         new_uil_group_data['uil_version'] = uil_version
         new_uil_group_data['create_by'] = ObjectId(new_uil_group_data['create_by'])

         # create uil and save
         new_uil_group = UILGroup(**new_uil_group_data)
         new_uil_group.save()

         response = jsonify(code=200, msg="ok", data={'name': new_uil_group_data['name'],
                                                     'uil_version': uil_version})
         response.status_code=200
         return response

      except ValidationError as err:
         print(err)
         response = jsonify(code=400, err="INVALID_INPUT")
         response.status_code = 400
         return response

      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response

class GetUILResource(Resource):
   def post(self):
      # TODO: Get detail of map task
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
   