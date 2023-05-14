from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask import request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError, validate
from app.models import User
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned

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

        # If the user is found and the password is correct, then update the last login time
        user.last_login_time = datetime.utcnow
        user.save()

        # Generate and set the tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        data = {
            "user_id":str(user.id),
            "username": user.username,
            "first_nae": user.first_name,
            "last_name": user.last_name,
            "nickname": user.nickname,
            "email": user.email,
        }
        response = jsonify(code=200,msg='ok',data=data)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return make_response(response,200)