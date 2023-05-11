from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates_schema
from app.models import Team, UserTeam, User
from bson import ObjectId
from flask import request, make_response, jsonify

class GetUserInputSchema(Schema):
    user_id = fields.String(required=True)

class PutUserInputSchema(Schema):
    # avatar = StringField(required=True)                               # group name
    user_ud = fields.String(required=True)                              # group name
    first_name = fields.String(required=False)                          # group name
    last_name = fields.String(required=False)                           # group name
    nickname = fields.String(required=False)                            # group name
    gender = fields.String(required=False)                              # group name
    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("EMPTY_REQUEST")
            
class PostUserTeamTeamInputSchema(Schema):
    team_id = fields.String(required=True)
    email = fields.Email(required=True)

class UserResource(Resource):
    
    def post():
        """Update the user profile
        """
        pass

    def put():
        """Update the user profile
        """
        try:
            in_schema = PutUserInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

    def get():
        """Get user profile
        """
        try:
            in_schema = GetUserInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            # TODO: Get user id from header token
            user_id = '645a59c3052f3ebedab52d78'
            # TODO: Check if the user is in the team

            user = User.objects(id=ObjectId(in_schema['user_id'])).first()
            if not user:
                return make_response(jsonify(code=404, err="USER_NOT_FOUND"), 404)
            data = {
                'user_id':str(user.id),
                'name': f'{user.first_name} {user.last_name}',
                'nickname': user.nickname,
                'email':user.email,
                'gender':user.gender
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

# class UserTeamResource(Resource):

#     def post():
#         """Invite a member into the team
#         """

#         try:
#             in_schema = PostUserTeamTeamInputSchema()
#             in_schema = in_schema.load(request.get_json())
#         except ValidationError as err:
#             return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
#         try:
#             # TODO: Get user id from header token
#             user_id = "645a59c3052f3ebedab52d78"

#             new_user_team = UserTeam(user_id=ObjectId(user_id),
#                                     team_id=in_schema['email'],
#                                     status='pending')





        
