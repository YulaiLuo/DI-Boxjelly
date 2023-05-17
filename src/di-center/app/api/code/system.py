from flask_restful import Resource
from flask import jsonify, request, make_response
from mongoengine.errors import DoesNotExist
from bson import ObjectId, json_util
from app.models import CodeSystem, ConceptGroup
from marshmallow import Schema, fields, ValidationError
import json

class PostCodeSystemInputSchema(Schema):
   team_id = fields.String(required=True)          # team id
   name = fields.String(required=True)
   description = fields.String(required=False)     # description of the version

class GetCodeSystemInputSchema(Schema):
   team_id = fields.String(required=True)
   code_system_id = fields.String(required=True)
   

class CodeSystemResource(Resource):

   def _handle_objectid(self,obj):
      if isinstance(obj, ObjectId):
         return str(obj)
      raise TypeError("Unserializable object {} of type {}".format(obj, type(obj)))

   def get(self):
      """return the list of code system concept given the team id

      Returns:
          _type_: _description_
      """

      try:
         in_schema = GetCodeSystemInputSchema()
         in_schema = in_schema.load(request.args)
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      
      try:
         code_system = CodeSystem.objects(id=ObjectId(in_schema['code_system_id'])).get()
      except DoesNotExist as err:
         return make_response(jsonify(code=404, err="CODE_SYSTEM_NOT_FOUND"), 404)
      # except MultipleObjectsReturned as err:
      #    return make_response(jsonify(code=400, err='MULTIPLE_CODE_SYSTEM_FOUND'), 400)

      try:

         pipeline = [
            {"$match": {"code_system_id": ObjectId(code_system.id)}},
            {"$lookup": {
               "from": "concept",
               "let": {"group_id": "$_id"},
               "pipeline": [
                  {"$match": {
                     "$and": [
                        {"$expr": {"$eq": ["$group_id", "$$group_id"]}},
                        {"$or": [{"child_concept_id": None}, {"child_concept_id": {"$exists": False}}]}
                     ]
                  }},
                  {"$addFields": {"id": "$_id"}},  
               ],
               "as": "concepts"}},
            {"$project": {
                  "_id": 0,
                  "group": "$name",
                  "group_id": "$_id",
                  "concepts.id": 1,
                  "concepts.name": 1,
                  "concepts.description": 1,
                  # "concepts.create_at":1   # has error
            }}
         ]

         groups = list(ConceptGroup.objects.aggregate(*pipeline))
         groups = json.loads(json.dumps(groups, default=self._handle_objectid))

         data = {
            'name':  code_system.name,
            'code_system_id': str(code_system.id),
            'create_at': code_system.create_at,
            'description': code_system.description,
            'groups':groups
         }

         response = jsonify(code=200, msg="ok", data=data)
         return make_response(response,200)
      
      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
      
   def update(self):
      # TODO: Update detail of code system
      pass

   def post(self):
      """
      Create new code system
      """
      try:
         # Create new code system API input schema
         in_schema = PostCodeSystemInputSchema()

         # load the data
         in_schema = in_schema.load(request.get_json())
      except ValidationError as err:
         print(err)
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      

      existing_code_system = CodeSystem.objects(team_id=ObjectId(in_schema['team_id'])).first()
      if existing_code_system:
         return make_response(jsonify(code=400, err="CODE_SYSTEM_EXIST_IN_TEAM"), 400)
      
      try:
         # TODO: read user id from request header
         # user_id = request.headers.get('user_id')
         user_id = '60c879e72cb0e6f96d6b0f65'

         # convert id string to object id
         in_schema['create_by'] = ObjectId(user_id)

         # create uil and save
         new_code_system = CodeSystem(
            team_id = in_schema['team_id'],
            name = in_schema['name'],
            description = in_schema['description'],
            create_by = ObjectId(user_id)
         )
         new_code_system.save()

         response = jsonify(code=200,msg="ok",
            data={
               'id':str(new_code_system.id),
               'name': new_code_system.name,
               'description': new_code_system.description
         })
         return make_response(response, 200)

      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code=500
         return response