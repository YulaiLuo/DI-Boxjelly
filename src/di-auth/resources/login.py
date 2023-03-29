from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError, validate
from pymongo.errors import OperationFailure

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
        """        
        
        # Validate the input data
        try:
            data = request.form
            login_data = EmailLoginSchema().load(data)
        except ValidationError:
            response = jsonify(code=400,err="INVALID_EMAIL_PASSWORD")
            response.status_code = 400
            return response

        # Get the email and password from the request
        email = login_data['email']
        password = login_data['password']

        # Find the user in the database
        print(email)
        user = self.mongo.db.users.find_one({'email': email})
        if not user:
            response = jsonify(code=404,err="USER_NOT_FOUND")
            response.status_code = 404
            return response

        # Check the password
        if not self.bcrypt.check_password_hash(user['password'], password):
            response = jsonify(code=401,err="INCORRECT_PASSWORD")
            response.status_code = 401
            return response

        # If the user is found and the password is correct, we start the transaction to update the last login time
        try:
            with self.mongo.cx.start_session() as session:
                with session.start_transaction():
                    
                    # Update the last login time
                    self.mongo.db.users.update_one({'email': email}, {'$set': {'last_login_time':datetime.utcnow()}})

                    # Generate the token here
                    access_token = create_access_token(identity=str(user['_id']))
                    refresh_token = create_refresh_token(identity=str(user['_id']))

                    # If user exist, password is correct and update success, return 200 status code 
                    response = jsonify(code=200,msg='ok')

                    # Set the JWT cookies in the response
                    set_access_cookies(response, access_token)
                    set_refresh_cookies(response, refresh_token)

                    response.status_code = 200
                    return response
        except OperationFailure:
            response = jsonify(code=400,err="Try Again Later")
            response.status_code = 400
            return response