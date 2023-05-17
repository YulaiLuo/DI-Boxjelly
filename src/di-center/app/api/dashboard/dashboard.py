from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import ConceptGroup, Concept, CodeSystem


class TopLeftResource(Resource):

    def get(self):
        return make_response(jsonify(code=200, msg="ok", data={
            "title": "This is a title",
            "total_number": "100",
            "delta": "+16% since last week",
            "percent": 0.16
        }))

class TopMiddleResource(Resource):

    def get(self):
        return make_response(jsonify(code=200, msg="ok", data={
            "title": "This is a title",
            "total_number": "100",
            "delta": "+16% since last week",
            "percent": 0.16
        }))

class TopRightResource(Resource):

    def get(self):
        return make_response(jsonify(code=200, msg="ok", data={
            "title": "This is a title",
            "total_number": "100",
            "delta": "+16% since last week",
            "percent": 0.16
        }))