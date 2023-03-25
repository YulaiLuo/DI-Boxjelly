from flask_restful import Resource, Api, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True, min_length=3, max_length=20)
    password = fields.Str(required=True, min_length=6, max_length=30)

user_schema = UserSchema()

class Login(Resource):
    def __init__(self, mongo, bcrypt):
        self.mongo = mongo
        self.bcrypt = bcrypt

    def post(self):
        try:
            user_data = user_schema.load(request.json)
        except ValidationError as e:
            return jsonify(code=400, msg=e.message, data={})

        users = self.mongo.db.users
        username = user_data['username']
        password = user_data['password']

        user = users.find_one({'username': username})

        if not user:
            return jsonify(code=404, msg='User not found',data={})

        if self.bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['_id']))
            self.mongo.db.tokens.insert_one({'type':'login',
                                                'status': 0,    # 0: valid, 1: expired
                                                'userid': user['_id'],
                                                'access_token': access_token,
                                                'generate_time': datetime.datetime.now(),
                                                'expire_time': datetime.datetime.now() + datetime.timedelta(min=15)})
            return jsonify(code=200,msg='success',data={'access_token': access_token})
        else:
            return jsonify(code=401,msg='Incorrect password',data={})
