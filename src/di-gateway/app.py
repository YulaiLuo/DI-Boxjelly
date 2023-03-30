from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Service address
service_map = {
    "auth": "http://127.0.0.1:8001/di_auth",
    "map": "http://127.0.0.1:8002/di_map"
}

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def gateway(path):
    # Get service name from path
    service_name = path.split("/")[0]

    if service_name not in service_map:
        response = jsonify(code=404 ,err="Service not found")
        response.status_code = 404
        return response

    target_url = service_map[service_name] + "/" + "/".join(path.split("/")[1:])
    print("target_url ",target_url)
    response = requests.request(
        method=request.method,
        url=target_url,
        headers={key: value for (key, value) in request.headers if key != "Host"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    return response.content, response.status_code, response.headers.items()

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 80
    app.run(debug=True, host=HOST, port=PORT)