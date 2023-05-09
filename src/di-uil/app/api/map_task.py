from flask import request, jsonify, send_file, Response
from flask_restful import Resource
from ..models import MapTask, MapItem
from ..schemas import CreateMapTaskInputSchema, DeleteMapTaskInputSchema, GetMapTaskInputSchema, GetAllMapTaskInputSchema
from marshmallow import ValidationError
from bson import ObjectId
from flask import current_app as app
from collections import Counter
from datetime import datetime
import math, csv, requests, threading, io
from io import StringIO
import codecs

class MapTasksResource(Resource):

   # Thread function to process the mapping task
   def map_items(self, map_url ,new_map_task, texts):

      # Invoke the map api to convert the raw text to snomed ct
      # res = requests.get('http://localhost:8003/map/translate', json={'texts': texts}).json()
      res = requests.post(f'{map_url}/map/translate', json={'texts': texts}).json()

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
         file = create_map_task_data['file']
         file_ext = file.filename.split('.')[-1].lower()

         texts = []

         if file_ext == 'txt':
            texts = file.readlines()
            texts = [text.decode('utf-8').strip() for text in texts]
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
            print("Invalid file format. Please upload a TXT or CSV file.")

         new_map_task = MapTask(
            num = len(texts),
            create_by = ObjectId(create_map_task_data['create_by']),
            # created_by = request.user_team_id
            file_name = file.filename,
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
         print(response)
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
         all_map_tasks = MapTask.objects(deleted=False).all()
         map_tasks = MapTask.objects(deleted=False).all().skip((page-1)*size).limit(size)
         # Convert the tasks to a list of dictionaries
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
                  "file_name": str(task.file_name),
               } 
               for task in map_tasks]
         }
         
         response = jsonify(code=200, msg="ok", data=data)
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
            'status': map_task.status,
            'items': items,
            'page': page,
            'size': size,
            'page_num': math.ceil(map_task.num/size)
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


class MapTaskMetaResource(Resource):
   def get(self, task_id):
      
      try:
         
         # map_task = MapTask.objects(id=task_id, deleted=False).first()
         # if not map_task:
         #    response = jsonify(code=404, err="MAP_TASK_NOT_FOUND")
         #    response.status_code = 404
         #    return response
         
         map_task = MapTask.objects(id=task_id, deleted=False).first()
         map_items = MapItem.objects(task_id=task_id).all()
         if not map_items:
            response = jsonify(code=404, err="MAP_ITEM_NOT_FOUND")
            response.status_code = 404
            return response
         
         # count the status of map items
         status_ctr = Counter([item.status for item in map_items])

         # Get the task meta
         data = {
            'id': task_id,       # task id
            'num': len(map_items),          # total item number
            'status': map_task.status,
            'create_at': map_task.create_at,
            'update_at': map_task.update_at,
            'num_success': status_ctr.get('success', 0),
            'num_failed': status_ctr.get('fail', 0),
            'num_reviewed': status_ctr.get('reviewed', 0)
         }


         response = jsonify(code=200, msg="ok", data=data)
         response.status_code=200
         return response
         

         
      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response
   

class DownloadMapTaskResource(Resource):

   def export_map_task_to_csv(self, map_task, map_items):

      csv_data = io.StringIO()
      csv_writer = csv.writer(csv_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

      # Get the meta data of map task
      total_num = map_task.num
      creation_date = map_task.create_at

      # Get the status count of map items
      status_ctr = Counter([item.status for item in map_items])
      success_count = status_ctr['success']
      fail_count = status_ctr['fail']
      reviewed_count = status_ctr['reviewed']

      # Meta Data
      csv_writer.writerow(['Total Number', 'Success Count', 'Failure Count', 'Review Count', 'Creation Date'])
      csv_writer.writerow([total_num, success_count, fail_count, reviewed_count, creation_date])

      # Add space between meta data and map items
      csv_writer.writerow([])

      # Map Items
      csv_writer.writerow(['Text', 'Output', 'Confidence', 'Source', 'Curated UIL', 'Status'])
      for item in map_items:
         map_info = item['mapped_info']
         if map_info:
            csv_writer.writerow([item['text'], 
                                 map_info[0]['sct_term'],
                                 map_info[0]['confidence'],
                                 'SNOMED_CT',
                                 '-',
                                 item['status']])
         else:
            csv_writer.writerow([item['text'], 
                                 '-',
                                 '-',
                                 '-',
                                 '-',                                    
                                 item['status']])

      csv_data.seek(0)
      return csv_data.getvalue().encode('utf-8')

   def get(self, task_id):
      try:
         map_task = MapTask.objects(id=task_id, deleted=False).first()
         if not map_task:
            response = jsonify(code=404, err="MAP_TASK_NOT_FOUND")
            response.status_code = 404
            return response
         
         map_items = MapItem.objects(task_id=task_id).all()
         if not map_items:
            response = jsonify(code=404, err="MAP_ITEM_NOT_FOUND")
            response.status_code = 404
            return response


         csv_data = self.export_map_task_to_csv(map_task, map_items)

         response = Response(csv_data, content_type='text/csv, utf-8')
         response.headers.set('Content-Disposition', 'attachment', filename=f"map_task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
         print(response.data)
         return response

      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response
      
