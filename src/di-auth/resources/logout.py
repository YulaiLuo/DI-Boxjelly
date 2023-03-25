from flask_restful import Resource
from flask import jsonify

class Logout(Resource):

    def __init__(self, mongo):
        self.mongo = mongo

    def post(self):
        response = jsonify(code=200,msg="success",data={})
        return response