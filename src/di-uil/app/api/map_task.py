from flask import request, Response, jsonify
from flask_restful import Resource
from ..models.map_task import MapTask
import requests


class CreateMapTaskResource(Resource):
   def post(self):
    
      file = request.files['file']

      # TODO: Validation check
      
      lines = file.readlines()
      
      new_map_task = MapTask(
         item_num = len(lines),
         create_by = 'kunxi'
         # created_by = request.user_team_id
      )

      new_map_task.save()

      # Invoke map api,发送一个map task过去
      print(new_map_task.id,str(new_map_task.id))

      response = jsonify(code=200,msg="ok", data={'id': str(new_map_task.id)})
      response.status_code = 200
      return response


class MapTaskDetailResource(Resource):
   def get(self):
      # TODO: Get detail of map task
      pass

class DeleteMapTaskResource(Resource):
   def post(self):
      # TODO: Get detail of map task
      pass

