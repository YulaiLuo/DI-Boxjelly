from flask_restful import Resource
from flask import jsonify, request

class Register(Resource):
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

        Returns:
            res: HTTP response
        """        
        users = self.mongo.db.users
        email = request.json['email']
        password = request.json['password']
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')

        if users.find_one({'email': email}):
            return jsonify(code=409, msg='Email already registered', data={})

        users.insert_one({'email': email, 'password': hashed_password})

        return jsonify(code=200, msg='success', data={})

