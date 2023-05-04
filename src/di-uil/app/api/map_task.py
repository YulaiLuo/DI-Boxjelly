from flask import request, jsonify
from flask_restful import Resource
from ..models import MapTask, MapItem
from ..schemas import CreateMapTaskInputSchema, DeleteMapTaskInputSchema, GetMapTaskInputSchema, GetAllMapTaskInputSchema
import threading
from marshmallow import ValidationError
from bson import ObjectId
import requests
from flask import current_app as app

class MapTasksResource(Resource):

   # Thread function to process the mapping task
   def map_items(self, map_url ,new_map_task, texts):

      # Invoke the map api to convert the raw text to snomed ct
      # res = requests.get('http://localhost:8003/map/translate', json={'texts': texts}).json()
      res = requests.get(f'{map_url}/map/translate', json={'texts': texts}).json()

      if res['msg']!='ok':
         new_map_task.status = 'fail'
         new_map_task.save()
         return
      
      # Create map items
      new_map_items = [MapItem(task_id = new_map_task.id,
                           text=texts[i],
                           status='success' if len(res['data'][str(i)])>0 else 'fail',
                           mapped_info=res['data'][str(i)]
                        ) for i in range(len(texts))
                     ]

      # TODO: find the UIL category in the past map items from database  

      # Save
      new_map_task.status = 'success'
      new_map_task.save()
      MapItem.objects.insert(new_map_items)

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
         texts = create_map_task_data['file'].readlines()
         texts = [text.decode('utf-8').strip() for text in texts]

         new_map_task = MapTask(
            num = len(texts),
            create_by = ObjectId(create_map_task_data['create_by']),
            # created_by = request.user_team_id
         )

         # Save map task
         new_map_task.save()

         # Create a new thread to process the mapping task
         map_url = app.config['MAP_SERVICE_URL']
         thread = threading.Thread(target=self.map_items, args=(map_url,new_map_task, texts))
         thread.start()

         response = jsonify(code=200,
                           msg="ok",
                           data={
                                 'id': str(new_map_task.id),
                                 'status': new_map_task.status
                           })
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
   

   def get(self):
      """
      Generate all the available map tasks

      Returns:
         Response: tasks list
      """
      schema = GetAllMapTaskInputSchema()
      
      try:
         input = schema.load(request.args)

         page = input['page']
         size = input['size']
         map_tasks = MapTask.objects(deleted=False).all().skip((page-1)*size).limit(size)

         # Convert the tasks to a list of dictionaries
         tasks = [
            {
                "id": str(task.id),
                "status": task.status,
                "num": task.num,
                "create_by": str(task.create_by),
                "create_at": task.create_at,
                "update_at": task.update_at
            }
            for task in map_tasks
         ]
         
         response = jsonify(code=200, msg="ok", data={'tasks': tasks})
         response.status_code = 200
         return response

      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response


class MapTaskResource(Resource):

   # Get map task detail by id
   def get(self, task_id):
      schema = GetMapTaskInputSchema()
      try:
         
         map_task_data = schema.load(request.args)

         map_task = MapTask.objects(id=task_id, deleted=False).first()
         if not map_task:
            response = jsonify(code=404, err="MAP_TASK_NOT_FOUND")
            response.status_code = 404
            return response

         page = map_task_data['page']  # min_value 1
         size = map_task_data['size']  # min_value 10
         map_items = MapItem.objects(task_id=task_id).skip((page-1)*size).limit(size)
         
         items = [{'text': map_item['text'], 'status': map_item['status'],'mapped_info': map_item['mapped_info']} for map_item in (mi.to_mongo().to_dict() for mi in map_items)]

         data = {
            'id': str(map_task.id),       # task id
            'num': map_task.num,          # total item number
            'status': map_task.status,
            'items': items
         }

         response = jsonify(code=200, msg="ok", data=data)
         response.status_code=200
         return response

      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response

   # soft delete the map task
   def delete(self, task_id):

      schema = DeleteMapTaskInputSchema()
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


class MapTaskListResource(Resource):
   def get(self):

      return 
