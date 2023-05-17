from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem, TaskBoard, Concept
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from flask import current_app as app
import requests, traceback

class PostMapTaskCurateSchema(Schema):
    # board_id = fields.String(required=True)
    # team_id = fields.String(required=True)
    map_item_id = fields.String(required=True)
    concept_id = fields.String(required=True)


class MapTaskCurateResource(Resource):
    
    def post(self):
        """Curate a map item to UIL
        """
        try:
            in_schema = PostMapTaskCurateSchema().load(request.get_json())
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        map_item = MapItem.objects(id=in_schema['map_item_id']).first()
        if not map_item:
            return make_response(jsonify(code=404, err="MAP_ITEM_NOT_FOUND"), 404)
        curated_concept = Concept.objects(id=in_schema['concept_id']).first()
        if not curated_concept:
            return make_response(jsonify(code=404, err="CONCEPT_NOT_FOUND"), 404)

        try:            
            
            map_item.curated_concept = curated_concept
            map_item.status = 'reviewed'
            
            # Send this curate to the mapper
            send_data = {
                'text': map_item.text,
                'curated_uil_name': map_item.curated_concept.name,
                'curated_uil_group': map_item.curated_concept.group.name,
            }
            print(send_data)
            response = requests.post(app.config['MAP_SERVICE_URL']+'/map/retrain', json=send_data)
            if response.status_code != 200:
                return make_response(jsonify(code=400, err="CURATING_FAIL"), 400)

            map_item.save()

            data = {
                "id": str(map_item.id),
                "text": map_item.text,
                "concept": curated_concept.name,
                "coonfidence": 1,   # curated item has default 100% confidence
                "source": curated_concept.code_system.name,
                "status": map_item.status,
                "concept_id": str(curated_concept.id),
                "source_id": str(curated_concept.code_system.id)
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            print(err)
            print(traceback.print_exc())
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)