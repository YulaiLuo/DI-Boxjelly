from flask_restful import Resource
from flask import send_from_directory, request, make_response, jsonify
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates, validates_schema

class GetAvatarInputSchema(Schema):
    url = fields.String(required=True)


class AvatarResource(Resource):

    def get(self):
        """send the avatar
        """
        try:
            in_schema = GetAvatarInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            return send_from_directory('/data/avatars', in_schema['url'])
        except FileNotFoundError as err:
            return make_response(jsonify(code=404, err="AVATAR_NOT_FOUND"), 404)
        except Exception as err: 
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)