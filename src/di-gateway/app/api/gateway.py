from flask import request, jsonify, request, Response, make_response
from flask import current_app as app
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from jwt.exceptions import ExpiredSignatureError
import requests


class GatewayResource(Resource):
    """
    In the gateway Service, except the login and register which does not 
    require the access token, all other requests are forwarded to 
    other services, if it can be found on the service map.


    Example:
        >>> from flask_restful import Api
        >>> api= Api()
        >>> api.add_resource(GatewayResource, '/<path:path>')
    """

    def __init__(self):
        self.service_map = app.config['SERVICE_MAP']

    @jwt_required()
    def _gateway(self, path):

        try:
            # Get user id from token
            user_id = get_jwt_identity()

            # Check if no user id (this means no valid token was provided)
            if not user_id:
                response = jsonify(code=401, err="TOKEN_EXPIRED",
                                   msg="Token has expired, please login again!")
                response.status_code = 401
                return response

            # Get service name from path
            service = path.split("/")[0]

            # Check if service is supported
            if service not in self.service_map:
                return make_response(jsonify(code=404, err="SERVICE_NOT_FOUND", msg="Service not found on end points, Please check your route"), 404)

            # Create target url
            target_url = self.service_map[service] + \
                "/" + "/".join(path.split("/")[1:])
            target_url = target_url.rstrip('/')  # Remove trailing slash

            # Create headers with user id from token
            headers = {
                "Content-Type": request.content_type,
                "User-ID": str(user_id),
            }

            # Forward request to target service
            response = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=request.get_data(),
                params=request.args,
                allow_redirects=False
            )

            return Response(response=response.content,
                            status=response.status_code,
                            headers={key: value for (key, value) in response.headers.items()})

        except ExpiredSignatureError:
            response = jsonify(code=401, err="TOKEN_EXPIRED",
                               msg="Token has expired, please login again")
            response.status_code = 401
            return response

    def get(self, path):
        """
        Forward all the GET request to the corresponding service

        Args:
            path (path): the path of the request

        Returns:
            Response: HTTP Response from the corresponding service
        """
        return self._gateway(path=path)

    def post(self, path):
        """
        Forward all the POST request to the corresponding service

        Args:
            path (path): the path of the request

        Returns:
            Response: HTTP Response from the corresponding service
        """
        return self._gateway(path=path)

    def put(self, path):
        """
        Forward all the PUT request to the corresponding service

        Args:
            path (path): the path of the request

        Returns:
            Response: HTTP Response from the corresponding service
        """
        return self._gateway(path=path)

    def delete(self, path):
        """
        Forward all the DELETE request to the corresponding service

        Args:
            path (path): the path of the request

        Returns:
            Response: HTTP Response from the corresponding service
        """
        return self._gateway(path=path)
