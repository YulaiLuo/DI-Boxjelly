from flask import Flask, jsonify, request
import requests
from api import api

app = Flask(__name__)
api.init_app(app)


if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT= 8003
    DEBUG = True

    app.run(debug=DEBUG, host=HOST, port=PORT)