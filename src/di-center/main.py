from app import create_app

app = create_app()

if __name__ == '__main__':

    HOST = '0.0.0.0'
    PORT = 8002
    DEBUG = True

    app.run(debug=DEBUG, host=HOST, port=PORT)