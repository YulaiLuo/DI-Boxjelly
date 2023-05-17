from flask import request, Response
from flask import current_app as app
from flask_restful import Resource
import requests
from flask_jwt_extended import set_access_cookies, set_refresh_cookies

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

        # Redirect login request to auth service
        response = requests.request(
                method=request.method,
                url=target_url,
                headers=request.headers,
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False, 
                timeout=20)
        
        # Create new response and set cookies
        new_response = Response(response=response.content,status=response.status_code)
        set_access_cookies(new_response, response.headers.get(app.config["JWT_ACCESS_COOKIE_NAME"]))
        set_refresh_cookies(new_response, response.headers.get(app.config["JWT_REFRESH_COOKIE_NAME"]))

        return new_response
