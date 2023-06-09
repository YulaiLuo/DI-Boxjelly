from flask_restful import Resource
from app.models import CodeSystem, ConceptGroup, Concept, Tag, ConceptVersion
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError
from flask import current_app as app
import requests

class CodeSystemVersionResource(Resource):

    def get(self):
        """
        Get all versions of the code system.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the list of code system versions
                    - code_systems (list): List of code system versions
                        - name (str): Name of the code system
                        - description (str): Description of the code system
                        - version (str): Version of the code system
                        - create_at (datetime): Timestamp of code system creation
        """
        user_id = request.headers.get('User-ID')

        code_systems = CodeSystem.objects(deleted=False).order_by('-create_at').all()

        data = {
            'code_systems':[{
                'name':code_system.name,
                'description': code_system.description,
                'version': code_system.version,
                'create_at': code_system.create_at,
            }for code_system in code_systems]
        }
        return make_response(jsonify(code=200, msg='ok', data=data))


        
        