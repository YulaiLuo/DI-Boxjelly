from flask_restful import Resource
from flask import jsonify, make_response
from collections import Counter
from app.models import MapTask, MapItem


class MapTaskMetaResource(Resource):
   def get(self, task_id):
      """Get the meta data of a map task for visualization

      Args:
          task_id (_type_): _description_

      Returns:
          _type_: _description_
      """
      
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

         return make_response(jsonify(code=200, msg="ok", data=data),200)
         
      except Exception as err:
         print(err)
         response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
         response.status_code = 500
         return response
   