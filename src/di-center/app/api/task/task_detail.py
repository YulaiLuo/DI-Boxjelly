from flask_restful import Resource
from flask import jsonify, request, make_response
from mongoengine.errors import DoesNotExist
from app.models import MapTask, MapItem
from marshmallow import Schema, fields, ValidationError, validates, validate, validates_schema
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
    min_accuracy = fields.Float(required=False, min_value=0.0, max_value=1.0)
    max_accuracy = fields.Float(required=False, min_value=0.0, max_value=1)
    ontology = fields.String(required=False)
    status = fields.String(required=False, validate=validate.OneOf(['all','reviewed', 'success', 'fail']))
    
    @validates_schema
    def validate_accuracies(self, data, **kwargs):
        """If the min_accuracy is larger then max_accuracy,
        Then raise a ValidateionError
        """
        if 'min_accuracy' in data and 'max_accuracy' not in data:
            raise ValidationError("Missing Minimum Accuracy")
        if 'max_accuracy' in data and 'min_accuracy' not in data:
            raise ValidationError("Missing Maximum Accuracy")
        if 'min_accuracy' in data and 'max_accuracy' in data:
            if data['min_accuracy'] > data['max_accuracy']:
                raise ValidationError("Minimum accuracy should not be greater than maximum accuracy")

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
            error_message = err.messages.get('_schema')[0]
            return make_response(jsonify(code=400, err="INVALID_INPUT", msg=error_message),404)
        
        try:
            task_id = in_schema['task_id']
            map_task = MapTask.objects(id=task_id, deleted=False).first()
            if not map_task:
                return make_response(jsonify(code=404, err="MAP_TASK_NOT_FOUND"),404)

            # Add filter conditions
            filter_conditions = {"task": task_id}
            if 'min_accuracy' in in_schema and 'max_accuracy' in in_schema:
               filter_conditions['accuracy__gte'] = in_schema['min_accuracy']
               filter_conditions['accuracy__lte'] = in_schema['max_accuracy']
            if 'ontology' in in_schema:
               filter_conditions['ontology'] = in_schema['ontology']
            if 'status' in in_schema:
               filter_conditions['status'] = in_schema['status']

            page = in_schema['page']  # min_value 1
            size = in_schema['size']  # min_value 10
            map_items = MapItem.objects(**filter_conditions).skip((page-1)*size).limit(size)
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
                'page_num': math.ceil(len(map_items)/size),
                'file_name': map_task.file_name
            }

            return make_response(jsonify(code=200, msg="ok", data=data),200)

        except Exception as err:
            print(traceback.format_exc())
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response

  
   