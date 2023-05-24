from flask_restful import Resource
from flask import jsonify, make_response, request
from collections import Counter
from app.models import MapTask, MapItem
from marshmallow import Schema, fields, ValidationError, validates
from bson import ObjectId

class GetMapTaskMetaSchema(Schema):
   task_id = fields.String(required=True)
                           

class MapTaskMetaResource(Resource):
   def get(self):
    try:
        in_schema = GetMapTaskMetaSchema()
        in_schema = in_schema.load(request.args)
    except ValidationError as err:
        return make_response(jsonify(code=400, err="INVALID_INPUT"),404)

    try:
        task_id = in_schema['task_id']
        map_task = MapTask.objects(id=ObjectId(task_id), deleted=False).first()
        if not map_task:
           response = jsonify(code=404, err="MAP_TASK_NOT_FOUND")
           response.status_code = 404
           return response

        pipeline = [
            {"$match": {"task": ObjectId(task_id)}},
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "ontology_count": {"$sum": {"$cond": [{"$eq": ["$ontology", 'SNOMED-CT']}, 1, 0]}}
            }}
        ]
        
        results = list(MapItem.objects.aggregate(*pipeline))

        status_ctr = {result["_id"]: result["count"] for result in results}
        ontology_ctr = {result["_id"]: result["ontology_count"] for result in results}

        data = {
            'id': task_id,
            'num': sum(status_ctr.values()),
            'status': map_task.status,
            'create_at': map_task.create_at,
            'update_at': map_task.update_at,
            'num_success': MapItem.objects(task=ObjectId(task_id), status='success').count(),
            'num_failed': MapItem.objects(task=ObjectId(task_id), status='fail').count(),
            'num_reviewed': MapItem.objects(task=ObjectId(task_id), status='reviewed').count(),
            'num_uil': MapItem.objects(task=ObjectId(task_id), ontology='UIL').count(),
            'num_snomed': MapItem.objects(task=ObjectId(task_id), ontology='SNOMED-CT').count(),
        }

        return make_response(jsonify(code=200, msg="ok", data=data),200)

    except Exception as err:
        print(err)
        response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
        response.status_code = 500
        return response
   