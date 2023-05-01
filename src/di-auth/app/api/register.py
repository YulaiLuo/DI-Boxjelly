from flask_restful import Resource
from flask import jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies

class EmailRegisterSchema(Schema):
    """
    A class to represent a Email Register Schema, used to validate the input data
    The input only have email, password and confirmed password

    Examples:
        >>> data = request.form
        >>> register_data = EmailRegisterSchema().load(data)
    """
    email = fields.Email(required=True, validate=validate.Length(min=6, max=128))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))
    confirm_password = fields.String(required=True, validate=validate.Length(min=6, max=128))

class EmailRegister(Resource):
    """
    A register flask restful api class.

    Args:
        mongo (PyMongo): The MongoDB connection object.
        bcrypt (Bcrypt): The Bcrypt object.

    Example:
        >>> register = Register(mongo, bcrypt)        
    """
    def __init__(self, mongo, bcrypt):
        self.mongo = mongo
        self.bcrypt = bcrypt

    def post(self):
        """
        User can register to the system by calling this endpoint.

        Args:
            email (str): the email of the user
            password (str): the original password(unhashed) of the user
            confirm_password (str): the original password(unhashed) of the user

        Returns:
            response (Response): HTTP Response

        Raises:
            ValidationError: If the input data is invalid

        Example:
            >>> url = <register_url>
            >>> payload = {'email': 'example@email.com', 'password': 'mypassword', 'confirm_password': 'mypassword'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 200, 'msg': 'success'} with status code 200, and set the access token and refresh token in the cookies
            
            >>> url = <register_url>
            >>> payload = {'email': 'example', 'password': 'mypassword', 'confirm_password': 'mypassword'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 400, 'msg': 'INVALID_EMAIL_PASSWORD'} with status code 400

            >>> url = <register_url>
            >>> payload = {'email': 'example@email.com', 'password': '12345678', 'confirm_password': '123456789'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 400, 'msg': 'PASSWORD_NOT_MATCH'} with status code 400
        """

        # Validate the input data
        try:
            data = request.form
            register_data = EmailRegisterSchema().load(data)
        except ValidationError:
            response = jsonify(code=400,err="INVALID_EMAIL_PASSWORD")
            response.status_code = 400
            return response

        # Get the email, password and confirm password from the request
        email = register_data['email']
        password = register_data['password']
        confirm_password = register_data['confirm_password']

        # Check if the password and confirm password are the same
        if password != confirm_password:
            response = jsonify(code=401,err="PASSWORD_NOT_MATCH")
            response.status_code = 401
            return response

        # Check if the email is already registered
        if self.mongo.db.users.find_one({'email': email}):
            response = jsonify(code=409,err="EMAIL_ALREADY_REGISTERED")
            response.status_code = 409
            return response

        # Hash the password and insert the user into the database
        result = self.mongo.db.users.insert_one({'email': email,
                                        'password': self.bcrypt.generate_password_hash(password).decode('utf-8'), 
                                        'create_time':datetime.utcnow(), 
                                        'last_login_time':datetime.utcnow()})
        
        # Check if the insert is successful
        if not result.acknowledged:
            response = jsonify(code=401,err="Try again later")
            response.status_code = 401
            return response

        # Set the access token and refresh token to the cookies
        response = jsonify(code=200,msg="success")

        # Create the access token and refresh token
        access_token = create_access_token(identity=str(result.inserted_id))
        refresh_token = create_refresh_token(identity=str(result.inserted_id))

        # Set the access token and refresh token to the cookies
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        response.status_code = 200
        return response
