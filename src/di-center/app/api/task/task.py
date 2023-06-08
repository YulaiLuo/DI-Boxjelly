import re
from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem, TaskBoard
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
from io import StringIO
import math, threading, requests, codecs, csv

class DeleteMapTaskInputSchema(Schema):
    task_id = fields.String(required=True)
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)

class PostMapTaskInputSchema(Schema):
   team_id = fields.String(required=True)
   board_id = fields.String(required=True)
   file = fields.Field(required=True)

   def _allowed_file(self, filename, allowed_extensions):
      return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in allowed_extensions

   @validates('file')
   def validate_file(self, file):
      if not self._allowed_file(file.filename, app.config['MAP_TASK_ALLOWED_EXTENSIONS']):
         raise ValidationError("FILE_NOT_ALLOWED")

class GetMapTaskInputSchema(Schema):
   team_id = fields.String(required=True)
   board_id = fields.String(required=True)
   page = fields.Integer(required=False,default=1, min_value=1)
   size = fields.Integer(required=False,default=20, min_value=10)

class MapTaskResource(Resource):
   
   """
   Resource for the map task list
   """
   def get(self):
      """
      Check the permission and get the map task list of a board

      Returns:
            Response: tasks list
      """
      in_schema = GetMapTaskInputSchema()
      
      try:
            user_id = request.headers.get('User-ID')

            in_schema = in_schema.load(request.args)

            page = in_schema['page']
            size = in_schema['size']
            board_id = in_schema['board_id']
            
            task_board = TaskBoard.objects(id=ObjectId(board_id),deleted=False).first()
            if not task_board:
               return make_response(jsonify(code=404, err="BOARD_NOT_FOUND"), 404)

            tasks = MapTask.objects(board=ObjectId(board_id),deleted=False).order_by('-create_at').skip((page - 1) * size).limit(size)
            map_task_count = MapTask.objects(board=task_board.id,deleted=False).count()

            # Retrieve the task creator's information
            task_creaters = {}
            auth_url = app.config['AUTH_SERVICE_URL']
            for task in tasks:
               task.create_by = str(task.create_by)
               if task.create_by not in task_creaters:
                  res = requests.get(auth_url+'/user', params={'user_id': task.create_by})
                  
                  # Update: check status code and decide what to do based on it
                  if res.status_code == 200:  # user found
                        task_creaters[task.create_by] = res.json()['data']['nickname']
                  elif res.status_code == 404:  # user not found
                        task_creaters[task.create_by] = 'USER REMOVED'

            # Convert the tasks to a list of dictionaries
            data = {
               'page': page,
               'size': size,
               'board_name':task_board.name,
               'board_description':task_board.description,
               'page_num': math.ceil(map_task_count/size),
               'tasks':[{
                  "id": str(task.id),
                  "status": task.status,
                  "num": task.num,
                  "create_by": task_creaters[task.create_by],
                  "nickname": task_creaters.get(task.create_by, "USER REMOVED"),
                  "create_at": task.create_at,
                  "update_at": task.update_at,
                  "file_name": str(task.file_name)
               }
               for task in tasks]
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
   
   # Thread function to process the mapping task
   def map_items(self, map_url ,new_map_task, texts):

      # TODO: Websocket

      # Invoke the map api to convert the raw text to snomed ct
      res = requests.post(f'{map_url}', json={'texts': texts})
      
      if res.status_code != 200:
         new_map_task.status = 'fail'
         new_map_task.save()
         return 
      
      res = res.json()
      mapper_name = res['data']['name']
      result = res['data']['result']

      new_map_items = [
         MapItem(task = new_map_task,
            text=texts[i],
            accuracy= None if not result[str(i)] else result[str(i)]['accuracy'],
            mapped_concept= None if not result[str(i)] else result[str(i)]['name'],
            status= None if not result[str(i)] else result[str(i)]['status'],
            ontology= None if not result[str(i)] else result[str(i)]['ontology'],
            extra= None if not result[str(i)] else result[str(i)]['extra']
         )for i in range(len(texts))
      ]

      # Save
      new_map_task.status = 'success'
      new_map_task.save()
      MapItem.objects.insert(new_map_items)

      # TODO: Websocket
 
   def post(self):
      """
      Create a new map task.

      Returns:
         Response: JSON response indicating the status of the request
      """

      # The data can come from file, form and ...etc
      data = {}
      data.update(request.files)
      data.update(request.form)

      try: 
         # load the data
         in_schema = PostMapTaskInputSchema()
         in_schema = in_schema.load(data)
      except ValidationError as err:
         print(err)
         return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

      try:
         file = in_schema['file']
         file_ext = file.filename.split('.')[-1].lower()

         texts = []

         if file_ext == 'txt':
            #texts = file.readlines()
            file_content = file.read().decode('utf-8')
            texts = re.findall(r'\d+\s+(.+)', file_content)
            #texts = [text.decode('utf-8').strip() for text in texts]
            if texts and codecs.BOM_UTF8.decode('utf-8') in texts[0]:
               texts[0] = texts[0].replace(codecs.BOM_UTF8.decode('utf-8'), '')

         elif file_ext == 'csv':
            file_content = file.read().decode('utf-8')
            if codecs.BOM_UTF8.decode('utf-8') in file_content:
               file_content = file_content.replace(codecs.BOM_UTF8.decode('utf-8'), '')
            text_stream = StringIO(file_content)
            reader = csv.reader(text_stream, delimiter=',', quotechar='"')
            # next(reader)  # Skip the header (if there is one)
            for row in reader:
               # Assuming the text data is in the first column of the CSV
               texts.append(row[0])
         else:
            return make_response(jsonify(code=400, err="INVALID_FILE_FORMAT"), 400)

         user_id = request.headers.get('User-ID')
         print("User-ID", user_id)
         new_map_task = MapTask(
               num = len(texts),
               create_by = ObjectId(user_id),
               # TODO
               mapper_name = 'MedCat',
               file_name = file.filename,
               team_id = ObjectId(in_schema['team_id']),
               board = ObjectId(in_schema['board_id'])
         )

         # Save map task
         new_map_task.save()

         # Create a new thread to process the mapping task
         map_url = app.config['MAP_SERVICE_URL']+'/predict'
         thread = threading.Thread(target=self.map_items, args=(map_url,new_map_task, texts))
         thread.start()

         data = {
            'id': str(new_map_task.id),
            'status': new_map_task.status
         }
         return make_response(jsonify(code=200, msg="ok", data=data), 200)

      except Exception as err:
         print(err)
         return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"),500)

   def delete(self):
      """
      Soft delete a map task in the database by changing the deleted as True

      Args:
         task_id (_type_): _description_

      Returns:
         _type_: _description_
      """
      try:
         in_schema = DeleteMapTaskInputSchema()
         in_schema = in_schema.load(request.args)
      except ValidationError as err:
         return make_response(jsonify(code=400, err="INVALID_INPUT"),404)

      try:
         # TODO: Check if the task is permitted to be deleted by this user

         # Change the deleted field as deleted
         MapTask.objects(id=ObjectId(in_schema['task_id'])).update_one(deleted=True)
         MapItem.objects(task=ObjectId(in_schema['task_id'])).update(deleted=True)

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
   