from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates, validates_schema
from app.models import Team, UserTeam, User
from flask import request, make_response, jsonify
from mongoengine.errors import DoesNotExist, NotUniqueError
from datetime import datetime, timedelta

class PostInviteInputSchema(Schema):
    team_id = fields.String(required=True)
    email = fields.Email(required=True)

    @validates('team_id')
    def validate_team_id(self, team_id):
        if not Team.objects(id=team_id).first():
            raise ValidationError('Team does not exist.')
        
    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if UserTeam.objects(team_id=data['team_id'],invite_email=data['email'], status='active').first():
            raise ValidationError('Email already invited.')
        
class GetInviteInputSchema(Schema):
    invitation = fields.String(required=True)

class PostAcceptInviteInputSchema(Schema):
    invitation = fields.String(required=True)   # UserTeam id
    username = fields.String(required=True)
    password = fields.String(required=True) #unhashed password
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    gender = fields.String(required=False,validate=validate.OneOf(['male','female','other']))

    @validates('username')
    def validate_username(self, username):
        if User.objects(username=username).first():
            raise ValidationError('Username already exists.')
    
    @post_load
    def make_nickname(self, data, **kwargs):
        if not data.get('nickname'):
            data['nickname'] = f"{data['first_name']} {data['last_name']}"
        return data

class InviteResource(Resource):
    def get(self):
        """Get invitation information by user_team_id(invite id)
        """

        try:
            in_schema = GetInviteInputSchema()
            in_schema = in_schema.load(request.args)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            user_team = UserTeam.objects(id=in_schema['invitation']).first()
        except DoesNotExist:
            return make_response(jsonify(code=404, err="INVITATION_NOT_FOUND"), 404)
        
        if datetime.utcnow() - user_team.create_at > timedelta(hours=24):
            return make_response(jsonify(code=400, err="INVITATION_EXPIRED"), 400)
        
        if user_team.status != "pending":
            return make_response(jsonify(code=400, err="INVITATION_USED"), 400)

        data = {
            # team information
            "team_id": str(user_team.team_id),
            "team_name": user_team.team_id.name,

            # Inviter information
            # "inviter_avatar": str(user_team.invite_by.first_name) + " " + str(user_team.invite_by.last_name),
            "inviter_name": str(user_team.invite_by.first_name) + " " + str(user_team.invite_by.last_name),

            # Invitation information
            "status": user_team.status,
            "join_time": user_team.join_time,
            "expire_at": user_team.create_at + timedelta(days=1)
        }
        return make_response(jsonify(code=200, msg="ok", data=data), 200)

    def post(self):
        """Invite a member into the team
        """

        try:
            in_schema = PostInviteInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            user_id = request.headers.get('User-ID')

            # Find if there are pending invitations, update the create time
            user_team = UserTeam.objects(
                team_id=in_schema['team_id'],
                invite_email=in_schema['email'],
                status='pending'
            ).first()

            if not user_team:
                # If the email is not in the team, create a new user_team invitation
                user_team = UserTeam(user_id=None,
                                team_id=in_schema['team_id'],
                                status='pending',
                                invite_by=user_id,
                                invite_email=in_schema['email']
                            )
            else:
                # If the email is already in the team, update the create time
                user_team.create_at = datetime.utcnow()
            
            user_team.save()

            # TODO: send an email to 'invite_email'
            #  send the id of user team to the email

            data = {
                'team_id': str(user_team.team_id),
                'invite_email': user_team.invite_email,
                'status': user_team.status,
                'role': user_team.role,
                'create_at': user_team.create_at,
                'expire_at': user_team.create_at + timedelta(days=1)
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

class AcceptInviteResource(Resource):

    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

    def post(self):
        """Accept a team invitation
        """

        try:
            in_schema = PostAcceptInviteInputSchema()
            in_schema = in_schema.load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            # If this invitation is used, return error
            user_team = UserTeam.objects(id=in_schema['invitation']).first()
            if user_team.user_id:
                return make_response(jsonify(code=400, err="USER_ALREADY_IN_TEAM"), 400)
            
            # Check if the invitation is still valid
            if datetime.utcnow() - user_team.create_at > timedelta(hours=24):
                return make_response(jsonify(code=400, err="INVITATION_EXPIRED"), 400)
            
            # Create a new user
            user = User(
                username=in_schema['username'],
                email=user_team.invite_email,
                password=self.bcrypt.generate_password_hash(in_schema['password']).decode('utf-8'),
                first_name=in_schema['first_name'],
                last_name=in_schema['last_name'],
                nickname=in_schema['nickname'],
                gender=in_schema.get('gender',None)
            )
            user.save()

            #  Update the invitation
            user_team.user_id = user.id
            user_team.status = 'active'
            user_team.join_time = datetime.utcnow
            user_team.save()

            data = {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'nickname': user.nickname,
                'team_id': str(user_team.team_id),
                'role': user_team.role
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
            
        except Exception as err:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
            