from datetime import datetime
from collections import Counter
from flask_restful import Resource
from flask import jsonify
from app.models import MapItem, MapTask
import csv, io


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

      with open(f"map_task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mode='w', newline='', encoding='utf-8') as csv_file:
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

      return csv_data.getvalue()

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

         response = Response(csv_data, content_type='text/csv')
         response.headers.set('Content-Disposition', 'attachment', filename=f"map_task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
         return response

      except Exception as err:
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response
      