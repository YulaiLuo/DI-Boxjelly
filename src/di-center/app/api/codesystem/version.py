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

        code_sysems = CodeSystem.objects(deleted=False).order_by('-create_at').all()

        users = {}
        auth_url = app.config['AUTH_SERVICE_URL']
        for creater_id in set([creater_id for creater_id in code_sysems.create_by]):
            users[creater_id] = requests.post(f'{auth_url}/auth/user?{user_id}={creater_id}').json()['data']

        data = {
            'code_systems':[{
                'name':code_system.name,
                'description': code_system.description,
                'create_by': users[code_system.create_by],
                'version': code_system.version,
                'create_at': code_system.create_at,
            }for code_system in code_sysems]
        }
        return make_response(jsonify(code=200, msg='ok', data=data))


        
        