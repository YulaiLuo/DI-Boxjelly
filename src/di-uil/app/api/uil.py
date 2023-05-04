from flask import request, jsonify
from flask_restful import Resource
from ..models import UILCategory, UIL, UILGroup
from ..schemas import CreateUILCategoryInputSchema, CreateUILInputSchema, CreateUILGroupInputSchema
from marshmallow import ValidationError
from collections import Counter
from bson import ObjectId

class CreateUILCategoryResource(Resource):
   def post(self, uil_version):
      
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
         
         # check if group id in the input schema
         group_name = ''
         if 'group_id' in new_uil_category_data:
            group_id = ObjectId(new_uil_category_data['group_id'])
            new_uil_category_data['group_id'] = group_id
            uil_group = UILGroup.objects(id=group_id).first()
            if uil_group:
               group_name=uil_group.name

         # create uil and save
         new_uil_category = UILCategory(**new_uil_category_data)
         new_uil_category.save()

         response = jsonify(
            code=200,
            msg="ok",
            data={
               'version': uil.version,
               'indication': new_uil_category.indication,
               'user_alias': new_uil_category.user_alias,
               'tags': new_uil_category.tags,
               # 'snomed_ct': new_uil_category.snomed_ct.,
               'group_name': group_name
         })
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

         response = jsonify(code=200,msg="ok", 
            data={
               'version': new_uil.version,
               'description': new_uil.description
         })
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

class CreateUILGroupResource(Resource):      

   def post(self, uil_version):
      # Create schema new map task API input schema
      schema = CreateUILGroupInputSchema()

      try:
         # load the data
         new_uil_group_data = schema.load(request.form)

         uil = UIL.objects(version=uil_version).first()
         if not uil:
            response = jsonify(code=404, err=" ")
            response.status_code = 404
            return response
         
         # convert id string to object id
         new_uil_group_data['uil_id'] = uil.id
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

   def get(self, uil_version):


      try:

         uil = UIL.objects(version=uil_version).first()

         if not uil:
            response = jsonify(code=404, err="UIL_NOT_FOUND")
            response.status_code = 404
            return response
         
         # uil_categories = UILCategory.objects(uil_id=uil.id).all()
         # uil_groups = UILGroup.objects(uil_id=uil.id).all()

         pipeline = [
            {
               "$match": {"uil_id": uil.id}
            },
            {
               "$lookup": {
                     "from": "uil_group",
                     "localField": "group_id",
                     "foreignField": "_id",
                     "as": "group"
               }
            },
            {
               "$project": {
                     "_id": 0,
                     "indication": 1,
                     "user_alias": 1,
                     "tags": 1,
                     "snomed_ct": 1,
                     "group_name": {'$arrayElemAt': ['$group.name', 0]},
                     "create_at": 1,
                     "update_at": 1,
                     # "create_by": 1
               }
            }
         ]

         uil_categories = UILCategory.objects.aggregate(*pipeline)

         # print(list(uil_categories))

         data = {
            'version':  uil.version,
            'description': uil.description,
            'categories':list(uil_categories)
         }

         response = jsonify(code=200, msg="ok", data=data)
         response.status_code=200
         return response
      
      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response

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



   