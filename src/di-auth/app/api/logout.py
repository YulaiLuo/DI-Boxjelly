from flask_restful import Resource
from flask import jsonify, request, make_response
from flask_jwt_extended import get_jwt, jwt_required
from app.models import BlackList
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates, validates_schema

class Logout(Resource):
    """
    A logout flask restful api class.

    Attributes:
        mongo (PyMongo): The MongoDB connection object.

    Example:
        >>> api = Api(app)
        >>> api.add_resource(Logout, '/auth/logout')
    """

    @jwt_required()
    def post(self):
        """
         User can log out of the system by calling this endpoint.

        Returns:
            res (Response): HTTP Response
        
        Example:
            >>> url = <logout_url>
            >>> headers: headers should have the cookie
            >>> requests.post(url, headers=headers)
            {'code': 200, 'msg': 'success'} with status code 200, and remove the access token and refresh token from the cookies
        """
        jti = get_jwt()['jti']
        
        # Save the jti to the blacklist
        BlackList(jti=jti).save()
                
        return make_response(jsonify(code=200,msg="success"),200)