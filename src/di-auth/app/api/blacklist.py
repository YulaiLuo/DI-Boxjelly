from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates, validates_schema
from app.models import BlackList
from flask import request, jsonify, make_response
from flask_jwt_extended import get_jwt

class PostInBlackListResource(Schema):
    jti = fields.String(required=True)

class CheckBlackListResource(Resource):

    def post(self):
        """
        Check if a token is in the blacklist.

        Args:
            jti (str): The JWT ID (jti) of the token to check.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - err (str): Error message, if any
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the result of the check
                    - in_blacklist (bool): True if the token is in the blacklist, False otherwise
        """
        try:
            in_schema = PostInBlackListResource().load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        in_black_list = BlackList.objects(jti=in_schema['jti']).first()
        if in_black_list:
            return make_response(jsonify(code=200, err=None, msg="success", data={'in_blacklist': True}), 200)

        return make_response(jsonify(code=200, err=None, msg="success", data={'in_blacklist': False}), 200)        
