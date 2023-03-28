from flask_restful import Resource
from flask import jsonify

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
            res: _description_
        """        
        response = jsonify(code=200,msg="success",data={})
        return response