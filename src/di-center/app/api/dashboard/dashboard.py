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

class HelloResource(Resource):

    def get(self):
        return make_response(jsonify(code=200, msg="ok", data={
            "hello": "This is a title",
        }))

class MapItemStatusRatioResource(Resource):

    def get(self):
        import random
        
        data = []
        years = [1995,1996,1997,1998,1999,2000,2001]
        for year in years:
            data.append({'year':str(year),'value':random.randint(1,10),'type':'success'})
        for year in years:
            data.append({'year':str(year),'value':random.randint(1,10),'type':'failed'})

        return make_response(jsonify(code=200, msg="ok", data=data))