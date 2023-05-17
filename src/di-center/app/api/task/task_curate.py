from flask_restful import Resource
from marshmallow import Schema, fields, ValidationError, validates
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem, TaskBoard
from bson import ObjectId
from mongoengine.errors import DoesNotExist

class PostMapTaskCurateSchema(Schema):
    board_id = fields.String(required=True)
    team_id = fields.String(required=True)
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
        
        try:
            map_item.curated_concept = in_schema['concept_id']
            map_item.statue = 'reviewed'
            map_item.save()

            # TODO: send this curate to the mapper
            # response = requests.post("http://di-mapper:xxxx/xxx")

            data = {
                "id": str(map_item.id),
                "text": map_item.text,
                "concept": map_item.curated_concept.name,
                "coonfidence": 1,   # curated item has default 100% confidence
                "source": map_item.concept.code_system.name,
                "status": map_item.statue,

                "concept_id": str(map_item.concept.id),
                "source_id": map_item.concept.code_system.id,
            }
            return make_response(jsonify(code=200, msg="ok", data=data), 200)
        except Exception as err:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)