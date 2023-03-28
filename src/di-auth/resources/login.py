from flask_restful import Resource
# from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError
# from datetime import datetime, timedelta

class UserSchema(Schema):
    email = fields.Str(required=True, min_length=3, max_length=20)
    password = fields.Str(required=True, min_length=6, max_length=30)

user_schema = UserSchema()

class Login(Resource):
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
        try:
            user_data = user_schema.load(request.json)
        except ValidationError as e:
            return jsonify(code=400, msg=e.messages, data={})

        users = self.mongo.db.users
        email = user_data['email']
        password = user_data['password']

        user = users.find_one({'email': email})

        if not user:
            response = jsonify(code=404, msg='User not found',data={})
            return response

        if self.bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['_id']))
            refresh_token = create_refresh_token(identity=str(user['_id']))

            response = jsonify(code=200, msg='success', data={'access_token':access_token, 'refresh_token':refresh_token})
            return response
        else:
            return jsonify(code=401, msg='Incorrect password',data={})
