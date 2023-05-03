from flask import request, jsonify
from flask_restful import Resource
from ..models.map_task import MapTask
from ..models.map_item import MapItem
from ..schema.map_task import CreateMapTaskInputSchema
import threading
from marshmallow import ValidationError


class CreateMapTaskResource(Resource):

   # Thread function to process the mapping task
   def map_items(self, new_map_task, lines):
      map_items = []
      for line in lines:
         new_map_item = MapItem(
            taskId = new_map_task.id,
            rawText = line.decode('utf-8').strip()
         )
         map_items.append(new_map_item)

      # TODO: Invoke the map api to convert the raw text to snomed ct
      

      # TODO: fine the UIL category in the past map items from database


      # Save map items
      MapItem.objects.insert(map_items)

   def post(self):

      # Create schema new map task API input schema
      schema = CreateMapTaskInputSchema()

      # The data can come from file, form and ...etc
      data = {}
      data.update(request.files)
      data.update(request.form)

      try: 
         # load the data
         create_map_task_data = schema.load(data)
         file = create_map_task_data['file']
         
         lines = file.readlines()
      
         new_map_task = MapTask(
            item_num = len(lines),
            create_by = 'kunxi'
            # created_by = request.user_team_id
         )

         # Save map task
         new_map_task.save()

         # Create a new thread to process the mapping task
         thread = threading.Thread(target=self.map_items, args=(new_map_task, lines))
         thread.start()

         response = jsonify(code=200,msg="ok", data={'id': str(new_map_task.id)})
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

class MapTaskDetailResource(Resource):
   def get(self):
      # TODO: Get detail of map task
      pass

class DeleteMapTaskResource(Resource):
   def post(self):
      # TODO: Get detail of map task
      pass

