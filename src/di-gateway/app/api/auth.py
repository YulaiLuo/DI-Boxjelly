from flask import request, Response
from flask import current_app as app
from flask_restful import Resource
import requests

class UserEmailLoginResource(Resource):
    """
    In the gateway Service, the login related routes are directly
    forwarded to the auth service without the need of access token


    Example:
        >>> api.add_resource(UserEmailLoginResource, '/auth/login/email')
    """    

    def __init__(self):
        self.service_map = app.config['SERVICE_MAP']

    def post(self):
        """
        Login with email and password
        Forwards the login post request to the auth service

        Returns:
            Response: HTTP Response from the auth service
        """

        target_url = self.service_map['auth'] + '/login/email'

        response = requests.request(
                method=request.method,
                url=target_url,
                headers={key: value for (key, value) in request.headers if key != "Host"},
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False, 
                timeout=3)
        
        return Response(response=response.content, 
                        status=response.status_code, 
                        headers={key: value for (key, value) in response.headers.items()})
    
class UserEmailRegisterResource(Resource):
    """
    In the gateway Service, the register related routes are directly
    forwarded to the auth service without the need of access token

    Example:
        >>> api.add_resource(UserEmailRegisterResource, '/auth/register/email')
    """    

    def __init__(self):
        self.service_map = app.config['SERVICE_MAP']

    def post(self):
        """
        Register with email, password and confirm password
        Forwards the login post request to the auth service

        Returns:
            Response: HTTP Response from the auth service
        """
        target_url = self.service_map['auth'] + '/register/email'

        response = requests.request(
                method=request.method,
                url=target_url,
                headers={key: value for (key, value) in request.headers if key != "Host"},
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False, 
                timeout=3)
        
        return Response(response=response.content, 
                        status=response.status_code, 
                        headers={key: value for (key, value) in response.headers.items()})
    
