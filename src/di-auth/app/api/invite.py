from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, post_load, validate, validates, validates_schema
from app.models import Team, UserTeam, User, Invitation
from flask import request, make_response, jsonify
from mongoengine.errors import DoesNotExist, NotUniqueError
from datetime import datetime
from flask import current_app as app


class InviteInputSchema(Schema):
    team_id = fields.String(required=True)

    @validates('team_id')
    def validate_team_id(self, team_id):
        if not Team.objects(id=team_id).first():
            raise ValidationError('Team does not exist.')


class GetInviteInputSchema(Schema):
    invitation = fields.String(required=True)


class PostAcceptInviteInputSchema(Schema):
    invite_token = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)  # unhashed password
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    gender = fields.String(
        required=False, validate=validate.OneOf(['Male', 'Female', 'Other']))

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
        """
        Generate an invitation token to invite members into the team.

        Args:
            team_id (str): The ID of the team to invite members to.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (str): The unique invitation token
        """

        try:
            in_schema = InviteInputSchema()  # team id
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:
            user_id = request.headers.get('User-ID')

            # Create a new Invitation
            invitation = Invitation(
                team_id=in_schema['team_id'],
                invite_by=user_id
            )
            invitation.save()

            # return the unique token as the "invitation link"
            return make_response(jsonify(code=200, msg="ok", data=str(invitation.invite_token)), 200)

        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)


class AcceptInviteResource(Resource):
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

    def post(self):
        """
        Accept a team invitation.

        Returns:
            res (Response): HTTP Response
                - code (int): HTTP status code
                - msg (str): Message indicating the status
                - data (dict): Dictionary containing the user's information and team details
                    - id (str): The user's ID
                    - username (str): The user's username
                    - email (str): The user's email
                    - first_name (str): The user's first name
                    - last_name (str): The user's last name
                    - nickname (str): The user's nickname
                    - team_id (str): The team's ID
                    - role (str): The user's role in the team
        """

        try:
            invite_token = request.form.get('invite_token')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            gender = request.form.get('gender')
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT", msg="Please ensure you've entered the information correctly!"), 400)

        # Create a dictionary with the retrieved data
        data = {
            'invite_token': invite_token,
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender
        }

        # Load the data into the schema
        in_schema = PostAcceptInviteInputSchema()
        in_schema = in_schema.load(data)

        try:
            # Retrieve the invitation
            invitation = Invitation.objects(
                invite_token=in_schema['invite_token']).first()

            # Check if the invitation is still valid
            if datetime.utcnow() > invitation.expiry_date:
                return make_response(jsonify(code=400, err="INVITATION_EXPIRED", msg="Invitation token expired"), 400)

            # Create a new user
            user = User(
                username=in_schema['username'],
                email=in_schema['email'],
                password=self.bcrypt.generate_password_hash(
                    in_schema['password']).decode('utf-8'),
                first_name=in_schema['first_name'],
                last_name=in_schema['last_name'],
                nickname=in_schema['nickname'],
                gender=in_schema.get('gender', None)
            )
            user.save()

            # Create a UserTeam entry
            user_team = UserTeam(
                user_id=user.id,
                team_id=invitation.team_id,
                invite_by=invitation.invite_by,
                join_time=datetime.utcnow()
            )
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
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
