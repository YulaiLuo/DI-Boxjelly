from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem, TaskBoard
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
import math, threading, requests, codecs, csv
from io import StringIO

class GetTaskBoardsInputSchema(Schema):
    team_id = fields.String(required=True)

class PostMapTaskInputSchema(Schema):
    team_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)

class MapTaskBoardsResource(Resource):

    def post(self):
        """Create a new task board
        """
        try:
            in_schema = PostMapTaskInputSchema()
            in_schema = in_schema.load(request.json)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            board = TaskBoard(
                team_id=ObjectId(in_schema['team_id']),
                name=in_schema['name'],
                description=in_schema.get('description','')
            ).save()
            data = {
                "id": str(board.id),
                "name": board.name,
                "description": board.description,
                "create_at": board.create_at,
                "update_at": board.update_at
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

    def get(self):
        """Get task board list
        """
        try:
            in_schema = GetTaskBoardsInputSchema()
            in_schema = in_schema.load(request.args)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            boards = TaskBoard.objects(team_id=ObjectId(in_schema['team_id']),deleted=False).all()

            data = {
                "boards": [{
                    "id": str(board.id),
                    "name": board.name,
                    "description": board.description,
                    "create_at": board.create_at,
                    "update_at": board.update_at
                }for board in boards]
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)


