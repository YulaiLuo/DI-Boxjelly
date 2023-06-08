from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem, TaskBoard
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError, validates
from io import StringIO

class GetTaskBoardsInputSchema(Schema):
    team_id = fields.String(required=True)

class PostMapTaskBoardsInputSchema(Schema):
    team_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=False)

class PutMapTaskBoardsInputSchema(Schema):
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)
    new_name = fields.String(required=True)
    new_description = fields.String(required=True)

class DeleteMapTaskBoardsInputSchema(Schema):
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)

class MapTaskBoardsResource(Resource):

    def put(self):
        """
        Modify a task board.

        Args:
            team_id (str): The ID of the team.
            board_id (str): The ID of the board to modify.
            new_name (str): The new name for the board.
            new_description (str): The new description for the board.

        Returns:
            Response: HTTP Response containing the modified board details.

        Raises:
            ValidationError: If the input data is invalid.
            OperationFailure: If the database operation failed.
        """
        try:
            in_schema = PutMapTaskBoardsInputSchema()
            in_schema = in_schema.load(request.json)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            board = TaskBoard.objects(id=in_schema['board_id'],team_id=ObjectId(in_schema['team_id']),deleted=False).first()
            if not board:
                return make_response(jsonify(code=404, err="BOARD_NOT_FOUND"), 404)
            board.name = in_schema['new_name']
            board.description = in_schema['new_description']
            board.save()
            data = {
                "id": str(board.id),
                "name": board.name,
                "description": board.description,
                "create_at": board.create_at,
                "update_at": board.update_at
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)

        except Exception as err:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

    def post(self):
        """
        Create a new task board.

        Args:
            team_id (str): The ID of the team.
            name (str): The name of the new board.
            description (str, optional): The description of the new board.

        Returns:
            Response: HTTP Response containing the details of the newly created board.

        Raises:
            ValidationError: If the input data is invalid.
            OperationFailure: If the database operation failed.
        """
        try:
            in_schema = PostMapTaskBoardsInputSchema()
            in_schema = in_schema.load(request.json)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            board = TaskBoard(
                team_id=ObjectId(in_schema['team_id']),
                name=in_schema['name'],
                description=in_schema.get('description','')
            )
            board.save()
            data = {
                "id": str(board.id),
                "name": board.name,
                "description": board.description,
                "create_at": board.create_at,
                "update_at": board.update_at
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

    def get(self):
        """
        Get the list of task boards.

        Args:
            team_id (str): The ID of the team.

        Returns:
            Response: HTTP Response containing the list of task boards.

        Raises:
            ValidationError: If the input data is invalid.
            OperationFailure: If the database operation failed.
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

    def delete(self):
        """
        Delete a task board.

        Args:
            team_id (str): The ID of the team.
            board_id (str): The ID of the board to delete.

        Returns:
            Response: HTTP Response indicating the success of the deletion.

        Raises:
            ValidationError: If the input data is invalid.
            OperationFailure: If the database operation failed.
        """
        try:
            in_schema = DeleteMapTaskBoardsInputSchema()
            in_schema = in_schema.load(request.args)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        try:
            TaskBoard.objects(id=ObjectId(in_schema['board_id'])).update_one(deleted=True)

            return make_response(jsonify(code=200, msg="ok"), 200)
        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

