from flask import Flask, request
import requests

app = Flask(__name__)

BACKEND_URL = ""

@app.route("/", methods=["GET", "POST", "PUT", "DELETE"])
def gateway():
    # Gateway implementation
    # ...
    return

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT= 80
    DEBUG = True

    print("-"*70)
    print("""Welcome to DI-Boxjelly\n
             Please open your browser to:
             http://{}:{}""".format(HOST,PORT))
    print("-"*70)

    app.run(debug=DEBUG, host=HOST, port=PORT)