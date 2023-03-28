from flask_restful import Resource

class Invite(Resource):
    """
    A invite flask restful api class.

    Args:
        mongo (PyMongo): The MongoDB connection object.
        mail (Mail): The Mail sending object.
    """    
    def __init__(self, mongo, mail):
        self.mongo = mongo
        self.collection = self.mongo['invite_code']
        self.mail = mail

    def get(self, access_token):
        """
        Get the invite code for the user with the given access token.

        Args:
            access_token (str): the accesstoken of the invitor
        """
        # Check if the access_token is valid
        if not self.collection.find_one({'access_token': access_token}):
            ...

