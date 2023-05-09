from flask_restful import Resource
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError, validates
from bson import ObjectId
from app.models import CodeSystem, Concept, ConceptGroup
from mongoengine.errors import DoesNotExist

class CreateConceptInputSchema(Schema):

   team_id = fields.String(required=True)                       
   name = fields.String(required=True)                               # latest name of the category
   description = fields.String(required=False)                               # latest user alias of the category
   group_id = fields.String(required=False)                               # id of the group

class ConceptResource(Resource):
   def post(self):
      """
      Create new concept given the team info
      """
      
      try:
         # Load data
         in_schema = CreateConceptInputSchema()
         in_schema = in_schema.load(request.form)
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      
      try:
         code_system = CodeSystem.objects(team_id=in_schema['team_id']).get()
      except DoesNotExist as err:
         return make_response(jsonify(code=404, err="CODE_SYSTEM_NOT_FOUND"), 404)

      try:
         # convert id string to object id
         # TODO: read user id from request header
         # user_id = request.headers.get('user_id')
         user_id = '60c879e72cb0e6f96d6b0f65'

         # create uil and save
         new_concept = Concept(code_system_id=code_system.id,
                           name = in_schema['name'], 
                           description = in_schema['description'], 
                           group_id = in_schema.get('group_id',None), 
                           create_by=ObjectId(user_id)
         )
         new_concept.save()

         return make_response(jsonify(code=201,msg="ok"),201)
   
      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response

   def get(self):
      # TODO: Get detail of map task
      pass

   def delete(self):
      # TODO: Get detail of map task
      pass

   def update(self):
      
      pass