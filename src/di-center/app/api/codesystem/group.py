from flask_restful import Resource
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError
from app.models import ConceptGroup, Concept, CodeSystem
from mongoengine.errors import DoesNotExist
import json

class GetConceptGroupInputSchema(Schema):
   group_id = fields.String(required=True)                  # code system id

class ConceptGroupResource(Resource):      

   def get(self):
      """
        Get group info and its concepts in the group.

        Args:
            group_id (str): The ID of the concept group.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the group and concept details
                    - group_id (str): The ID of the concept group
                    - group_name (str): The name of the concept group
                    - concepts (list): List of concept details
                        - id (str): The ID of the concept
                        - name (str): The name of the concept
                        - description (str): The description of the concept
                        - update_at (datetime): The update timestamp of the concept
                        - create_at (datetime): The creation timestamp of the concept
        """
      try:
         # load the data
         in_schema = GetConceptGroupInputSchema()
         in_schema = in_schema.load(request.args)
         
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

      try:
         # concept groups
         group = ConceptGroup.objects(id=ObjectId(in_schema['group_id'])).first()
         if not group:
            return make_response(jsonify(code=404, err="GROUP_NOT_FOUND", msg="Group is not found!"), 404)

         concepts = Concept.objects(group=ObjectId(in_schema['group_id']), child_concept=None).all()

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
       
   
