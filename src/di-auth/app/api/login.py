from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask import request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError, validate
from app.models import User, UserTeam, Team
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from flask import current_app as app

class EmailLoginSchema(Schema):
    """
    A class to represent a Email Login Schema, used to validate the input data
    The input only have email and password

    Example:
        >>> data = request.form
        >>> login_data = EmailLoginSchema().load(data)
    """
    email = fields.Email(required=True, validate=validate.Length(min=6, max=128))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))

class EmailLogin(Resource):
    """
    A class to represent a Login API

    Args:
        mongo (PyMongo): PyMongo instance used to connect to MongoDB
        bcrypt (Bcrypt): Bcrypt instance used to hash password

    Examples:
        >>> mongo = PyMongo()
        >>> bcrypt = Bcrypt()
        >>> login = Login(mongo, bcrypt)
    """    
    def __init__(self, mongo, bcrypt):
        self.mongo = mongo
        self.bcrypt = bcrypt

    def post(self):
        """
        User log in 

        Args:
        email (str): the email of the user
        password (str): the original password(unhashed) of the user

        Returns:
            Response: HTTP Response

        Raises:
            ValidationError: If the input data is invalid
            OperationFailure: If the database operation failed
        """
        # Validate the input data
        try:
            in_schema = EmailLoginSchema()
            in_schema = in_schema.load(request.form)
        except ValidationError:
            response = jsonify(code=400,err="INVALID_EMAIL_PASSWORD")
            return make_response(response,400)

        # Find the user in the database
        try:
            user = User.objects(email=in_schema['email']).get()
        except DoesNotExist:
            response = jsonify(code=404,err="USER_NOT_FOUND")
            return make_response(response,404)
        except MultipleObjectsReturned:
            response = jsonify(code=500,err="MULTIPLE_USERS_FOUND")
            return make_response(response,500)
            
        # Check the password
        if not self.bcrypt.check_password_hash(user.password, in_schema['password']):
            response = jsonify(code=401,err="INCORRECT_PASSWORD")
            return make_response(response,401)

        # TODO: There will only be one team, to support multiple team, change the following lines
        try:
            user_team = UserTeam.objects(user_id=user.id, status='active').first()
            if user_team.status == 'absent':
                response = jsonify(code=401,err="USER_NOT_IN_TEAM")
                return make_response(response,401)
            elif user_team.status == 'pending':
                response = jsonify(code=401,err="ACTIVATE_ACCOUNT_FIRST")
                return make_response(response,401)
        except DoesNotExist:
            response = jsonify(code=404,err="USER_TEAM_NOT_FOUND")
            return make_response(response,404)
        
        # TODO: The system only need to support one team
        team = user_team.team_id

        # Generate and set the tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        data = {
            "user":{
                "id":str(user.id),
                "avatar": user.avatar,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "nickname": user.nickname,
                "email": user.email
            },
            "team":{
                "id": str(team.id),
                "name": team.name,
                "role": user_team.role,
                "status": user_team.status,
                "join_time": user_team.join_time,
                "last_login_time": user_team.last_login_time
            }
        }
        user_team.last_login_time = datetime.utcnow
        user_team.save()

        # Add access token and refresh token cookies in headers
        response = jsonify(code=200,msg='ok',data=data)
        response.headers.add(app.config["JWT_ACCESS_COOKIE_NAME"],access_token)
        response.headers.add(app.config["JWT_REFRESH_COOKIE_NAME"],refresh_token)

        res = make_response(response,200)
        return res