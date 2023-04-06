"""
This module is responsible for user authentication and authorization.

The main function including: login, register, logout, and invite member.

Example:
    >>> from flask import Flask
    >>> from app_config import app_config
    >>> app = Flask(__name__)
    >>> app.run()
"""

from app import create_app

app = create_app()

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT = 8001
    DEBUG = True

    app.run(debug=DEBUG, host=HOST, port=PORT)