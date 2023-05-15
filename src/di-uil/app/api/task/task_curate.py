from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates

class PostMapTaskCurateSchema(Schema):
    board_id = fields.String(required=True)
    team_id = fields.String(required=True)
    map_item_id = fields.String(required=True)
    concept_id = fields.String(required=True)

class MapTaskCurateResource(Resource):
    
    def post(self):
        """Curate a map item to UIL
        """
        # Redirect the curate result to the mapper
        
        pass
    
    def get(self):
        pass
