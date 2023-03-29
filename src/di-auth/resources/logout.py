from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies

class Logout(Resource):
    """
    A logout flask restful api class.

    Attributes:
        mongo (PyMongo): The MongoDB connection object.

    Example:
        >>> logout = Logout(mongo)
        >>> logout.post()
    """

    def __init__(self, mongo):
        self.mongo = mongo

    def post(self):
        """
         User can log out of the system by calling this endpoint.

        Returns:
            res (Response): HTTP Response
        """        
        response = jsonify(code=200,msg="success")
        response.status_code = 200

        # This step remove the access token and refresh token from the cookies on the client side
        unset_jwt_cookies(response)

        # TODO: add the jti token to the blacklist

        return response