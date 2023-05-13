from flask_restful import Resource
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError, validates
from bson import ObjectId
from app.models import CodeSystem, Concept, ConceptGroup
from mongoengine.errors import DoesNotExist, NotUniqueError, MultipleObjectsReturned

class CreateConceptInputSchema(Schema):

   code_system_id = fields.String(required=True)                       
   group_id = fields.String(required=False)                               # id of the group
   name = fields.String(required=True)                               # latest name of the category
   description = fields.String(required=False)                               # latest user alias of the category

class AllConceptsInputSchema(Schema):
   code_system_id = fields.String(required=True)                  # code system id

class AllConceptResource(Resource):
   def get(self):
      """Retrieve all concepts given a code system id
      """
      try:
         in_schema = AllConceptsInputSchema()
         in_schema = in_schema.load(request.args)
      except ValidationError as err:
         print(err)
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      
      try:
         code_system = CodeSystem.objects(id=in_schema['code_system_id']).get()
      except DoesNotExist as err:
         print(err)
         return make_response(jsonify(code=404, err="CODE_SYSTEM_NOT_FOUND"), 404)
      except MultipleObjectsReturned as err:
         print(err)
         return make_response(jsonify(code=400, err='MULTIPLE_CODE_SYSTEM_FOUND'), 400)
      try:
         concepts = Concept.objects(code_system_id=code_system.id).all()
         data = {
            'concepts':[{
                  'id':str(concept.id),
                  'name':concept.name,
                  'description':concept.description,
                  'create_at':concept.create_at,
                  'update_at':concept.update_at
            }for concept in concepts]
         }

         return make_response(jsonify(code=200, msg="ok", data=data), 200)
      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

class ConceptResource(Resource):
   def post(self):
      """Create new concept given the team info
      """
      try:
         # Load data
         in_schema = CreateConceptInputSchema()
         in_schema = in_schema.load(request.get_json())
      except ValidationError as err:
         print(err)
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      
      try:
         code_system = CodeSystem.objects(id=in_schema['code_system_id']).get()
      except DoesNotExist as err:
         print(err)
         return make_response(jsonify(code=404, err="CODE_SYSTEM_NOT_FOUND"), 404)

      try:
         # convert id string to object id
         # TODO: read user id from request header
         # user_id = request.headers.get('user_id')
         user_id = '642d169c6f21e6617508fca9'

         # create uil and save
         new_concept = Concept(code_system_id=code_system.id,
                           name = in_schema['name'], 
                           description = in_schema.get('description',None), 
                           group_id = in_schema.get('group_id',None), 
                           create_by=ObjectId(user_id)
         )
         new_concept.save()

         return make_response(jsonify(code=201,msg="ok",data={"id":str(new_concept.id),"name":new_concept.name, "description":new_concept.description}),201)
      except NotUniqueError as err:
         print(err)
         return make_response(jsonify(code=400, err="NOT_UNIQUE_NAME"), 400)
   
      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 400)


   def get(self):
      # TODO: Get detail of a concept
      pass

   def delete(self):
      # TODO: Delete a concept
      pass

   def put(self):
      # TODO: Update a concept
      pass