from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
import math, threading, requests, codecs, csv
from io import StringIO

class GetMapTaskBoardInputSchema(Schema):
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)
    page = fields.Integer(required=False,default=1, min_value=1)
    size = fields.Integer(required=False,default=20, min_value=10)


class MapTaskBoardResource(Resource):
    """
    Resource for the map task list
    """

    def get(self):
        """
        Check the permission and get the map task list of a workspace

        Returns:
            Response: tasks list
        """
        in_schema = GetMapTaskBoardInputSchema()
        
        try:
            # TODO: check the permission
            # user_id = request.headers.get('user_id')
            # team_id = team_id

            in_schema = in_schema.load(request.args)

            page = in_schema['page']
            size = in_schema['size']
            board_id = in_schema['board_id']
            all_map_tasks = MapTask.objects(board_id=ObjectId(board_id),deleted=False).order_by('-id').all()
            if not all_map_tasks:
                return make_response(jsonify(code=404, err="MAP_TASKS_NOT_FOUND"),404)
            map_tasks_page = all_map_tasks.skip((page-1)*size).limit(size)
            
            # Convert the tasks to a list of dictionaries
            # TODO: search pipeline
            data = {
                'page': page,
                'size': size,
                'page_num': math.ceil(len(all_map_tasks)/size),
                'tasks':[{
                    "id": str(task.id),
                    "status": task.status,
                    "num": task.num,
                    "create_by": str(task.create_by),
                    "create_at": task.create_at,
                    "update_at": task.update_at,
                    "file_name": str(task.file_name)
                }
                for task in map_tasks_page]
            }
            
            response = jsonify(code=200, msg="ok", data=data)
            response.status_code = 200
            return response
        
        except ValidationError as err:
            print(err)
            response = jsonify(code=400, err="INVALID_INPUT")
            response.status_code = 400
            return response
            
        except Exception as err:
            print(err)
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response
    
    