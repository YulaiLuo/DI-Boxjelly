"""
This module is responsible for user authentication and authorization.

The main function including: login, register, logout, and invite member.

Example:
    >>> from flask import Flask
    >>> from app_config import app_config
    >>> app = Flask(__name__)
    >>> app.run()
"""

# if __name__ == '__main__':

#     HOST = '0.0.0.0'
#     PORT= 8001
#     DEBUG = True

#     app.run(debug=DEBUG, host=HOST, port=PORT)

    # import sys
    # service_name = sys.argv[1]
    # # service_host = sys.argv[2]
    # service_port = int(sys.argv[2])

    # print(service_name, service_port)

    # register_service_to_consul(service_name, service_port,consul_host='127.0.0.1',consul_port=8500)

    # app.run(debug=True, host=service_host, port=service_port)

from app import create_app

app = create_app()

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT = 8001
    DEBUG = True

    app.run(debug=DEBUG, host=HOST, port=PORT)