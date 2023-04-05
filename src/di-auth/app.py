"""
This module is responsible for user authentication and authorization.

The main function including: login, register, logout, and invite member.

Example:
    >>> from flask import Flask
    >>> from app_config import app_config
    >>> app = Flask(__name__)
    >>> app.run()
"""
import consul
from flask import Flask, jsonify
from resources import api, mongo, bcrypt, mail, jwt
import socket

# Initialize the configuration of flask app
import app_config
app = Flask(__name__)
app.config.from_object(app_config)

api.init_app(app)
mongo.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)
jwt.init_app(app)

@app.route('/health')
def health():
    response = jsonify({'code': '200', 'msg': 'success'})
    response.status_code = 200
    return response

# def register_service_to_consul(service_name, service_port, consul_host='127.0.0.1', consul_port=8500):

#     c = consul.Consul(host=consul_host, port=consul_port)

#     # Get this machine's IP address
#     ip_address = '127.0.0.1'
#     # ip_address = socket.getaddrinfo(socket.gethostname(), None)

#     c.agent.service.register(
#         service_name,
#         address=ip_address,
#         port=service_port,
#         check=consul.Check.http(
#             f'http://{ip_address}:{service_port}/health',
#             interval='10s',
#             timeout='1s'
#         )
#     )

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT= 8001
    app.run(debug=True, host=HOST, port=PORT)

    # import sys
    # service_name = sys.argv[1]
    # # service_host = sys.argv[2]
    # service_port = int(sys.argv[2])

    # print(service_name, service_port)

    # register_service_to_consul(service_name, service_port,consul_host='127.0.0.1',consul_port=8500)

    # app.run(debug=True, host=service_host, port=service_port)