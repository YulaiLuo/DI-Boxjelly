from flask_restful import Resource
from flask_jwt_extended import jwt_required

class Invite(Resource):
    def __init__(self, mongo, mail):
        self.mongo = mongo
        self.collection = self.mongo['invite_code']
        self.mail = mail

    def get(self, access_token):
        """Get the invite code for the user with the given access token.

        Args:
            access_token (_type_): _description_
        """
        # Check if the access_token is valid
        if not self.collection.find_one({'access_token': access_token}):
            ...

    def post(self):
        ...