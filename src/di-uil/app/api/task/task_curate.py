from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates

class PostMapTaskCurateSchema(Schema):
    board_id = fields.String(required=True)
    team_id = fields.String(required=True)
    mapped_item_id = fields.String(required=True)    

class MapTaskCurateResource(Resource):
    
    def post(self):

        pass
