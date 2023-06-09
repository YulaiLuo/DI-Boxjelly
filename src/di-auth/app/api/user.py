from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates_schema, validate
from app.models import Team, UserTeam, User
from bson import ObjectId
from flask import request, make_response, jsonify
from mongoengine.errors import DoesNotExist
from app.models import User

class GetUserInputSchema(Schema):
    user_id = fields.String(required=True)

class PutUserInputSchema(Schema):
    # avatar = StringField(required=True)
    first_name = fields.String(required=False,min_len=1)
    last_name = fields.String(required=False,min_len=1)
    nickname = fields.String(required=False,min_len=1)
    gender = fields.String(required=False,validate=validate.OneOf(['Male','Female','Other']))                              # group name
    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("EMPTY_REQUEST")
            
class UserResource(Resource):

    def put(self):
        """
        Update the user profile.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the updated user details
                    - user_id (str): The ID of the updated user
                    - name (str): The updated name of the user
                    - nickname (str): The updated nickname of the user
                    - email (str): The email of the user
                    - gender (str): The updated gender of the user
        """
        try:
            in_schema = PutUserInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        user_id = request.headers.get('User-ID')

        try:
            # Update the user's profile
            User.objects(id=user_id).update_one(**in_schema)           
            updated_user = User.objects(id=user_id).first()
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
        data = {
            'user_id':str(updated_user.id),
            'name': f'{updated_user.first_name} {updated_user.last_name}',
            'nickname': updated_user.nickname,
            'email':updated_user.email,
            'gender':updated_user.gender
        }
        return make_response(jsonify(code=200, msg="ok", data=data), 200)

    def get(self):
        """
        Get user profile.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the user profile
                    - user_id (str): The ID of the user
                    - name (str): The name of the user
                    - nickname (str): The nickname of the user
                    - email (str): The email of the user
                    - gender (str): The gender of the user
                    - avatar (str): The avatar of the user (default if not available)
        """
        try:
            in_schema = GetUserInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            # to check if the requester is in the team
            user_id = request.headers.get('User-ID')

            user = User.objects(id=in_schema['user_id']).first()
            if not user:
                return make_response(jsonify(code=404, err="USER_NOT_FOUND", msg="The user is not found!"), 404)
            data = {
                'user_id':str(user.id),
                'name': f'{user.first_name} {user.last_name}',
                'nickname': user.nickname,
                'email':user.email,
                'gender':user.gender,
                'avatar': 'default' if not user.avatar else user.avatar
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

        