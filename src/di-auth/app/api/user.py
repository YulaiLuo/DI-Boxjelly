from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask import current_app, request, jsonify
from marshmallow import Schema, fields, ValidationError, validate
from pymongo.errors import OperationFailure
import jwt

class UserSchema(Schema):
    """
    A class to represent a User Schema, used to validate the input data
    The input should contain first name, last name, and gender fields.

    Example:
        >>> data = request.form
        >>> user_data = UserSchema().load(data)
    """

    email = fields.Email(required=True, validate=validate.Length(min=6, max=128))
    password = fields.String(required=True, validate=validate.Length(min=6, max=128))

    firstName = fields.String(required=True, validate=validate.Length(min=1, max=128))
    lastName = fields.String(required=True, validate=validate.Length(min=1, max=128))
    gender = fields.String(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    

class UserCreate(Resource):
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

        Example:
            >>> url = <login_url>
            >>> payload = {'email': 'example@email.com', 'password': 'mypassword'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 200, 'msg': 'success'} with status code 200, and set the access token and refresh token in the cookies

            >>> url = <login_url>
            >>> payload = {'email': 'example', 'password': 'mypassword'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 400, 'msg': 'INVALID_EMAIL_PASSWORD'} with status code 400

            >>> url = <login_url>
            >>> payload = {'email': 'correct@email.com', 'password': 'incorrect_password'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 401, 'msg': 'INCORRECT_PASSWORD'} with status code 401

            >>> url = <login_url>
            >>> payload = {'email': 'user_not_exist@email.com', 'password': 'correct_password'}
            >>> headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            >>> requests.post(url, data=payload, headers=headers)
            {'code': 404, 'msg': 'USER_NOT_FOUND'} with status code 404
        """

        # Validate the input data
        try:
            data = request.form
            register_data = UserSchema().load(data)
        except ValidationError:
            response = jsonify(code=400,err="INVALID_DATA")
            response.status_code = 400
            return response

        # Get the email and password from the request
        email = register_data['email']
        password = register_data['password']

        firstName =  register_data['firstName']
        lastName = register_data['lastName']
        gender = register_data['gender']
        
        # Verify if the URL is valid and not expired
        token = request.args.get('token')
        if not token:
            response = jsonify(code=400, err="INVALID_TOKEN")
            response.status_code = 400
            return response
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            response = jsonify(code=400, err="TOKEN_EXPIRED")
            response.status_code = 400
            return response
        except jwt.InvalidTokenError:
            response = jsonify(code=400, err="INVALID_TOKEN")
            response.status_code = 400
            return response
        
        if payload['email'] != email:
            response = jsonify(code=400, err="INVALID_TOKEN")
            response.status_code = 400
            return response
        
        # Check if the user already exists in the database
        if self.mongo.db.users.find_one({'email': email}):
            response = jsonify(code=400,err="USER_ALREADY_EXISTS")
            response.status_code = 400
            return response
        
        
    


        

        # If the user is found and the password is correct, we start the transaction to update the last login time
        try:
            with self.mongo.cx.start_session() as session:
                with session.start_transaction():
                    
                    # Insert the user data
                    self.mongo.db.users.insert_one({
                        'email': email,
                        'password': password,
                        'firstName': firstName,
                        'lastName': lastName,
                        'gender': gender,
                        'created_at': datetime.utcnow()
                    })
                    # Create access and refresh tokens
                    access_token = create_access_token(identity=email)
                    refresh_token = create_refresh_token(identity=email)

                    # Set the JWT cookies in the response
                    response = jsonify(code=200,msg='ok')
                    set_access_cookies(response, access_token)
                    set_refresh_cookies(response, refresh_token)

                    response.status_code = 200
                    return response

        except OperationFailure as e:
            response = jsonify(code=500, err="DATABASE_ERROR")
            response.status_code = 500
            return response


                    # If user exist, password is correct and update success, return 200 status code 
        #             response = jsonify(code=200,msg='ok')

        #             # Set the JWT cookies in the response
        #             set_access_cookies(response, access_token)
        #             set_refresh_cookies(response, refresh_token)

        #             response.status_code = 200
        #             return response
        # except OperationFailure:
        #     response = jsonify(code=400,err="TRANSACTION_FAILED")
        #     response.status_code = 400
        #     return response