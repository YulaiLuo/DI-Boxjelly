from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<p>Weclome to Ontoserver Microservice</p>"

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT= 82
    DEBUG = True

    print("-"*70)
    print("""Welcome to DI-Boxjelly\n
             Please open your browser to:
             http://{}:{}""".format(HOST,PORT))
    print("-"*70)

    app.run(debug=DEBUG, host=HOST, port=PORT)