from flask_restful import Resource
from app.controllers import MedcatController
from marshmallow import Schema, fields, ValidationError, validates
from flask import request, make_response, jsonify
import traceback

medcat_controller = MedcatController()

class GetPredictResourceInputSchema(Schema):
    texts = fields.List(fields.String(), required=True)
    
class PostRetrainInputSchema(Schema):
    text = fields.String(required=True)

    curated_uil_name = fields.String(required=True)
    curated_uil_group = fields.String(required=True)

class PostResetInputSchema(Schema):
    pass

class PredictResource(Resource):

    def post(self):
        try:
            in_schema = GetPredictResourceInputSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            data = medcat_controller.predict(in_schema)
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(traceback.format_exc())
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

class RetrainResource(Resource):

    def post(self):
        try:
            in_schema = PostResetInputSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            data = medcat_controller.retrain(in_schema)
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)


class ResetResource(Resource):

    def post(self):
        try:
            in_schema = PostRetrainInputSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            data = medcat_controller.reset(in_schema)
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

