from flask import Response, request
from flask_restful import Resource
from flask import jsonify

class Register(Resource):
    def __init__(self, mongo, bcrypt):
        self.mongo = mongo
        self.bcrypt = bcrypt
    
    def post(self):
        users = self.mongo.db.users
        username = request.json['username']
        password = request.json['password']
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')

        user = users.find_one({'username': username})

        if user:
            return jsonify(code=409, msg='Username already exists')

        users.insert_one({'username': username, 'password': hashed_password})

        return jsonify(code=200, msg='success')

