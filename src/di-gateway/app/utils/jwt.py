from flask import jsonify
from flask_jwt_extended import JWTManager
from jwt.exceptions import InvalidTokenError

def init_jwt(app):
    """
    Initialize the JWTManager

    Args:
        app (Flask): The Flask app
    """

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def custom_unauthorized_response(header_error):
        response = jsonify(code=401 ,err="UNAUTHORIZED", msg="Missing or invalid token")
        response.status_code = 401
        return response

    @jwt.expired_token_loader
    def custom_expired_token_response(header_error):
        response = jsonify(code=401 ,err="TOKEN_EXPIRED", msg="Token has expired")
        response.status_code = 401
        return response

    @jwt.revoked_token_loader
    def custom_revoked_token_response(header_error):
        response = jsonify(code=401 ,err="TOKEN_REVOKED", msg="Token has been revoked")
        response.status_code = 401
        return response

    @jwt.invalid_token_loader
    def custom_invalid_token_response(header_error):
        response = jsonify(code=401 ,err="INVALID_TOKEN_TYPE", msg="Invalid token type")
        response.status_code = 401
        return response

    @app.errorhandler(InvalidTokenError)
    def custom_jwt_decode_error_response(header_error):
        response = jsonify(code=401 ,err="WRONG_TOKEN", msg="Error decoding the token")
        response.status_code = 401
        return response