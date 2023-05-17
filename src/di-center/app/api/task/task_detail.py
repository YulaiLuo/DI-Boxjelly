from flask_restful import Resource
from flask import jsonify, request, make_response
from mongoengine.errors import DoesNotExist
from app.models import MapTask, MapItem
from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
import math, threading, requests, codecs, csv
from io import StringIO
from bson import ObjectId
import traceback

class GetMapTaskInputSchema(Schema):
    task_id = fields.String(required=True)
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)
    page = fields.Integer(required=False,default=1, min_value=1)
    size = fields.Integer(required=False,default=20, min_value=10)


class MapTaskDetailResource(Resource):
    """
    The MapTaskResource class is used to handle the request of map task.
    """
    # Get map task detail by id
    def get(self):
        
        try:
            in_schema = GetMapTaskInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            print(err)
            return make_response(jsonify(code=400, err="INVALID_INPUT"),404)
        
        try:
            task_id = in_schema['task_id']
            map_task = MapTask.objects(id=task_id, deleted=False).first()
            if not map_task:
                return make_response(jsonify(code=404, err="MAP_TASK_NOT_FOUND"),404)

            page = in_schema['page']  # min_value 1
            size = in_schema['size']  # min_value 10
            map_items = MapItem.objects(task=task_id).skip((page-1)*size).limit(size)
            items = [
                {'map_item_id': str(item.id),
                 'text':item.text, 
                 'accuracy': item.accuracy,
                 'mapped_concept': item.mapped_concept,
                 'ontology':item.ontology, 
                 'status':item.status,
                 'curate':None if not item.curated_concept else item.curated_concept.name,
                 'extra':None if not item.extra else item.extra
                 } for item in map_items ]


            data = {
                'id': str(map_task.id),       # task id
                'status': map_task.status,
                'items': items,
                'page': page,
                'size': size,
                'page_num': math.ceil(map_task.num/size),
                'file_name': map_task.file_name
            }

            response = jsonify(code=200, msg="ok", data=data)
            response.status_code=200
            return response

        except Exception as err:
            print(traceback.format_exc())
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response

  
   