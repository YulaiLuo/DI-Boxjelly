from flask_restful import Resource
from app.models import CodeSystem, ConceptGroup, Concept, Tag, ConceptVersion
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError
from flask import current_app as app
import requests

class CodeSystemVersionResource(Resource):

    def get(self):
        """Get all version of code system
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


        
        