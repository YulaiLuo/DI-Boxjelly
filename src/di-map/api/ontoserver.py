from flask_restful import Resource
from flask import jsonify, request
import requests
from marshmallow import Schema, fields, ValidationError, validate

class TranslateSchema(Schema):
    code = fields.Str(required=True)

class Translate(Resource):

    def __init__(self):
        pass

    def get(self):

        # Get the data from the request
        # try:
        #     translate_data = TranslateSchema().load(request.args)
        # except ValidationError as e:
        #     response = jsonify(code=400,err="INVALID_PARAMETER",msg="The parameter is invalid")
        #     response.status_code = 400
        #     return response
        
        # Get the code from the request
        code = request.args.get('code')
        # code = translate_data['code']

        # Get the translation from the Ontoserver
        url = "https://r4.ontoserver.csiro.au/fhir/ConceptMap/$translate"
        params = {'url':'http://ontoserver.csiro.au/fhir/ConceptMap/automapstrategy-default',
                'system': 'http://ontoserver.csiro.au/fhir/CodeSystem/codesystem-terms',
                'code': f'{code}',
                'target': 'http://snomed.info/sct?fhir_vs'}
        res = requests.get(url = url, params = params)

        return res.json()