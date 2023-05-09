from flask_restful import Resource
from flask import jsonify, request, make_response
from marshmallow import Schema, fields, ValidationError
from mongoengine.errors import DoesNotExist
from app.models import MapTask, MapItem
import math

class DeleteMapTaskInputSchema(Schema):
   id = fields.String(required=True)

class GetMapTaskInputSchema(Schema):
   team_id = fields.String(required=True)
   board_id = fields.String(required=True)
   page = fields.Integer(required=False,default=1, min_value=1)
   size = fields.Integer(required=False,default=20, min_value=10)

class MapTaskResource(Resource):
   """
   The MapTaskResource class is used to handle the request of map task.
   """

   # Get map task detail by id
   def get(self, task_id):
      """
      Get map task items by id

      Args:
         task_id (String): the id of the task

      Returns:
          _type_: _description_
      """
      in_schema = GetMapTaskInputSchema()
      try:
         in_schema = in_schema.load(request.args)
         page = in_schema['page']  # min_value 1
         size = in_schema['size']  # min_value 10

      except ValidationError:
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

      try:
         map_task = MapTask.objects(id=task_id, deleted=False).get()
      except DoesNotExist:
         return make_response(jsonify(code=404, err="MAP_TASK_NOT_FOUND"), 200)


      map_items = MapItem.objects(task_id=task_id).skip((page-1)*size).limit(size)
      
      items = [{'text': map_item['text'], 'status': map_item['status'],'mapped_info': map_item['mapped_info']} for map_item in (mi.to_mongo().to_dict() for mi in map_items)]

      data = {
         'id': str(map_task.id),       # task id
         'status': map_task.status,
         'items': items,
         'page': page,
         'size': size,
         'page_num': math.ceil(map_task.num/size)
      }

      return make_response(jsonify(code=200, msg="ok", data=data), 200)

  
   def delete(self, task_id):
      """
      Soft delete a map task in the database by changing the deleted as True

      Args:
          task_id (_type_): _description_

      Returns:
          _type_: _description_
      """

      in_schema = DeleteMapTaskInputSchema()
      try:
         # TODO: Check if the task is permitted to be deleted by this user

         # TODO: Check if the task is deleted

         # Change the deleted field as deleted
         MapTask.objects(id=task_id).update_one(deleted=True)

         response = jsonify(code=200, msg="ok")
         response.status_code = 200
         return response

      except ValidationError as err:
         print(err)
         response = jsonify(code=400, err="INVALID_INPUT")
         response.status_code = 400
         return response

      except Exception as err:
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response
      
 