from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import unset_jwt_cookies

class Logout(Resource):
    """
    A logout flask restful api class.

    Attributes:
        mongo (PyMongo): The MongoDB connection object.

    Example:
        >>> api = Api(app)
        >>> api.add_resource(Logout, '/di-auth/logout', resource_class_args=(mongo,))
    """

    def __init__(self, mongo, jwt):
        self.mongo = mongo
        self.jwt = jwt

    def post(self):
        """
         User can log out of the system by calling this endpoint.

        Returns:
            res (Response): HTTP Response
        
        Example:
            >>> url = <logout_url>
            >>> headers: headers should have the cookie
            >>> requests.post(url, headers=headers)
            {'code': 200, 'msg': 'success'} with status code 200, and remove the access token and refresh token from the cookies
        """
        # TODO: check if the header has the cookie
        # TODO: add the tokens to the blacklist on the server side

        # Generate the success logout response
        response = jsonify(code=200,msg="success")
        response.status_code = 200

        # This step remove the access token and refresh token from the cookies on the client side
        unset_jwt_cookies(response)

        return response