from flask_restful import Resource
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError
from app.models import ConceptGroup, Concept, CodeSystem
from mongoengine.errors import DoesNotExist
import json

class PostConceptGroupInputSchema(Schema):
   name = fields.String(required=True)
   code_system_id = fields.String(required=True)                  # code system id

class GetConceptGroupInputSchema(Schema):
   group_id = fields.String(required=True)                  # code system id

class DeleteConceptGroupInputSchema(Schema):
   group_id = fields.String(required=True)                  # group id

class UpdateConceptGroupInputSchema(Schema):
   group_id = fields.String(required=True)
   new_name = fields.String(required=True)

class ConceptGroupResource(Resource):      

   def get(self):
      try:
         # load the data
         in_schema = GetConceptGroupInputSchema()
         in_schema = in_schema.load(request.args)
         
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

      try:
         # concept groups
         group = ConceptGroup.objects(id=in_schema['group_id']).first()
         if not group:
            return make_response(jsonify(code=404, err="GROUP_NOT_FOUND"), 404)

         concepts = Concept.objects(group_id=in_schema['group_id'], child_concept_id=None).all()

         response = jsonify(code=200, msg="ok", data={
            'group_id': in_schema['group_id'],
            'group_name': group.name,
            'concepts': [{'id':str(concept.id),
                   'name':concept.name, 
                   'description':concept.description, 
                   'update_at': concept.update_at, 
                   'create_at':concept.create_at} for concept in concepts]
         })
         return make_response(response,200)

      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
       
   def post(self):

      try:
         # load the data
         in_schema = PostConceptGroupInputSchema()
         in_schema = in_schema.load(request.get_json())
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      
      try:
         code_system = CodeSystem.objects(id=in_schema['code_system_id']).get()
      except DoesNotExist as err:
         return make_response(jsonify(code=404, err="CODE_SYSTEM_NOT_FOUND"), 404)
      except MultipleObjectsReturned as err:
         return make_response(jsonify(code=400, err='MULTIPLE_CODE_SYSTEM_FOUND'), 400)
      
      
      # TODO: read user id from request header
      # user_id = request.headers.get('user_id')
      user_id = '60c879e72cb0e6f96d6b0f65'

      try:
         # convert id string to object id
         in_schema['create_by'] = ObjectId(user_id)

         # create uil and save
         new_concept_group = ConceptGroup(name=in_schema['name'], 
                                          code_system_id=code_system.id, 
                                          create_by=in_schema['create_by'])
         new_concept_group.save()

         response = jsonify(code=201, msg="ok", data={
            'id': str(new_concept_group.id),
            'name': new_concept_group.name,
         })
         return make_response(response,201)

      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

   def delete(self):
      try:
         # load the data
         in_schema = DeleteConceptGroupInputSchema()
         in_schema = in_schema.load(request.args)
         
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      
      try:

         # If the group still have items, it cannot be deleted
         concepts = Concept.objects(group_id=in_schema['group_id']).first()
         if concepts:
            return make_response(jsonify(code=400, err="GROUP_NOT_EMPTY"), 400)
         

         # If the group does not exist, cannot remove it
         concept_group = ConceptGroup.objects(id=in_schema['group_id']).first()
         if not concept_group:
            return make_response(jsonify(code=404, err="GROUP_NOT_FOUND"), 404)

         # if the group is empty and exist, delete it
         # concept groups
         concept_group.delete()

         response = jsonify(code=200, msg="ok", data={
            'id': str(concept_group.id),
            'name': concept_group.name
         })
         return make_response(response,200)

      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
       
   def put(self):

      try:
         # load the data
         in_schema = UpdateConceptGroupInputSchema()
         in_schema = in_schema.load(request.get_json())
         
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
      try:

         # If the group does not exist, cannot update it
         concept_group = ConceptGroup.objects(id=in_schema['group_id']).first()
         if not concept_group:
            return make_response(jsonify(code=404, err="GROUP_NOT_FOUND"), 404)

         # update group name
         old_name = concept_group.name
         concept_group.name = in_schema['new_name']
         concept_group.save()

         response = jsonify(code=200, msg="ok", data={
            'id': str(concept_group.id),
            'new_name': concept_group.name,
            'old_name':old_name
         })
         return make_response(response,200)

      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
       
