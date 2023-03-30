from flask import Flask, request, jsonify
import requests
from flask_jwt_extended import JWTManager, jwt_required,set_access_cookies, set_refresh_cookies
app = Flask(__name__)

DI_AUTH_URL = "http://di_auth:8001"
DI_ONTOSERVER_URL = "http://di_ontoserver:8001"


jwt_settings = {
    'JWT_TOKEN_LOCATION': ['cookies'],
    "JWT_SECRET_KEY":"di",
    "JWT_ALGORITHM":"HS256",
    'JWT_ACCESS_TOKEN_EXPIRES':3600,
}
# Initialize
app.config.update(jwt_settings)
jwt = JWTManager(app)

# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response

@app.route('/login', methods=['POST'])
def login():
    """
    Login a user.
    Returns:
        Reponse: if status code is 200, return the user info and access token.
                 if status code is not 200, return the error message.
    """
    # send the login request to the login service
    s_response = requests.post(f'{DI_AUTH_URL}/di_auth/login', json=request.get_json())
    print(s_response)
    if s_response.status_code == 200:

        # get the cookies from the service response
        access_token = s_response.json().get("data").get("access_token")
        refresh_token = s_response.json().get("data").get("refresh_token")

        c_response = jsonify(code=200, msg='success')

        # set tthe cookies into the client response
        set_access_cookies(c_response, access_token)
        set_refresh_cookies(c_response, refresh_token)
        return c_response
    else:
        return s_response.json(), s_response.status_code


@app.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    Try: curl -X POST http://localhost:8000/register -H 'Content-Type: application/json' -d '{"email":"diboxjelly@gmail.com","password":"123"}'
    Returns:
        Response: if status code is 200, return the user info and access token.
                  if status code is not 200, return the error message.
    """
    print("in register")
    # send the register request to the register service
    print("request:", request.json)
    response = requests.post(f'{DI_AUTH_URL}/di_auth/register', json=request.get_json())
    print(response)

    # send the response from the register service to the client
    return jsonify(response.json()), response.status_code

@app.route("/logout", methods=["POST"])
@jwt_required
def logout():
    """
    Logout a user.
    Returns:
        Response: if status code is 200, user logout success
                  if status code is not 200, return the error message.
    """
    # send the logout request to the register service
    response = requests.post(f'{DI_AUTH_URL}/di_auth/logout', json=request.get_json())

    # send the response from the logout service to the client
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT= 8000
    DEBUG = True

    print("-"*70)

    app.run(debug=DEBUG, host=HOST, port=PORT)