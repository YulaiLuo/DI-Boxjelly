from flask_restful import Api
from .medcat import Translate
from .mapper import PredictResource, RetrainResource, ResetResource

def init_api(app):
    """
    Initialize the API, adding all routes to the Flask app.

    Args:
        app (Flask): The Flask app
    """

    # Create the API instance
    api = Api()

    # Add route
    api.add_resource(Translate, '/map/translate')

    # Add mapper resources
    api.add_resource(PredictResource, '/map/predict', )
    api.add_resource(RetrainResource, '/map/retrain')
    api.add_resource(ResetResource, '/map/reset')

    # Initialize the API
    api.init_app(app)



