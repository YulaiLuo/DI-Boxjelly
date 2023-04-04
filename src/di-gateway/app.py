from flask import Flask, request, jsonify
from flask_cors import CORS
# from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required
import requests
from jwt.exceptions import InvalidTokenError

app = Flask(__name__)

# load_dotenv()
# app.config.from_pyfile('.env')
import app_config
app.config.from_object(app_config)

jwt = JWTManager(app)
corsa = CORS(app, supports_credentials=True)

service_map = {
    "auth": "http://di_auth:8001/auth",
    "map": "http://di_map:8003/map"
}
# service_map = {
#     "auth": "http://localhost:8001/auth",
#     "mapengine": "http://localhost:8003/mapengine"
# }

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

@app.route("/auth/login/<string:login_way>", methods=["POST"])
def login(login_way):
    if login_way == "email":
        target_url = service_map["auth"] + "/login/email"
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False, 
            timeout=5)

        return response.content, response.status_code, response.headers.items()
    
    response = jsonify(code=404 ,err="SERVICE_NOT_FOUND", msg=f"Login by {login_way} is not supported")
    response.status_code = 404
    return response

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
# @jwt_required()
def gateway(path):

    service = path.split("/")[0]

    if service not in service_map:
        response = jsonify(code=404 ,err="SERVICE_NOT_FOUND", msg=f"Service {service} is not supported")
        response.status_code = 404
        return response

    # if not request.path.startswith("/auth/login") and request.method == 'POST':
    #     jwt_required()(lambda: None)()

    target_url = service_map[service] + "/" + "/".join(path.split("/")[1:])
    print("target_url ",target_url)
    response = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for (key, value) in request.headers if key != "Host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        timeout=5)

    return response.content, response.status_code, response.headers.items()

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 8000
    app.run(debug=True, host=HOST, port=PORT)