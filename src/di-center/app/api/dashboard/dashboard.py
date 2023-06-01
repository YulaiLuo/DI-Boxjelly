from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import ConceptGroup, Concept, CodeSystem, MapItem, MapTask
from flask import current_app as app
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
from marshmallow import Schema, fields, ValidationError, validates, validate
import requests

class GetMapItemStatusRatioSchema(Schema):
    range = fields.String(required=False, missing='day', validate=validate.OneOf(['day', 'week', 'month']))


def get_start_of_weeks():
    """
    Get the start of this week and last week

    Returns:
        datetime: the start of this week
        datetime: the start of last week
    """
    start_of_this_week = datetime.now() + relativedelta(weekday=MO(-1))
    start_of_last_week = start_of_this_week - relativedelta(weeks=1)
    return start_of_this_week, start_of_last_week

class TopLeftResource(Resource):

    def get(self):

        # Calculate the start of this week and the start of the last week
        start_of_this_week, start_of_last_week = get_start_of_weeks()
        
        task_count = MapTask.objects(deleted=False).count()
        
        this_week_count = MapTask.objects(deleted=False, create_at__gte=start_of_this_week).count()
        last_week_count = MapTask.objects(deleted=False, create_at__gte=start_of_last_week, create_at__lt=start_of_this_week).count()

        delta = this_week_count - last_week_count

        return make_response(jsonify(code=200, msg="ok", data={
            "title": f"Total Task submitted: {task_count}",
            "total_number": f"This week submit: {this_week_count}",
            "delta": f"{'+' if delta>0 else ''}{delta} since last week",
            "percent": delta/last_week_count*100 if last_week_count > 0 else 0
        }))

class TopMiddleResource(Resource):

    def get(self):

        # Calculate the start of this week and the start of the last week
        start_of_this_week, start_of_last_week = get_start_of_weeks()

        this_week_count = MapItem.objects(deleted=False, create_at__gte=start_of_this_week).count()
        last_week_count = MapItem.objects(deleted=False, create_at__gte=start_of_last_week, create_at__lt=start_of_this_week).count()

        delta = this_week_count - last_week_count
        total_count = MapItem.objects(deleted=False).count()

        return make_response(jsonify(code=200, msg="ok", data={
            "title": f"Total texts mapped: {total_count}",
            "total_number": f"This week mapped: {this_week_count}",
            "delta": f"{'+' if delta>0 else ''}{delta} since last week",
            "percent": delta/last_week_count*100 if last_week_count > 0 else 0
        }))

class TopRightResource(Resource):

    def get(self):

        # Calculate the start of this week and the start of the last week
        start_of_this_week, start_of_last_week = get_start_of_weeks()

        this_week_count = MapItem.objects(status='reviewed', deleted=False, create_at__gte=start_of_this_week).count()
        last_week_count = MapItem.objects(status='reviewed', deleted=False, create_at__gte=start_of_last_week, create_at__lt=start_of_this_week).count()
        
        delta = this_week_count - last_week_count
        total_count = MapItem.objects(status='reviewed', deleted=False).count()

        return make_response(jsonify(code=200, msg="ok", data={
            "title": f"Total curated texts: {total_count}",
            "total_number": f"This week curated: {this_week_count}",
            "delta": f"{'+' if delta>0 else ''}{delta} since last week",
            "percent": delta/last_week_count*100 if last_week_count > 0 else 0
        }))

class HelloResource(Resource):

    def get(self):
        user_id = request.headers.get('User-ID')
        if user_id is None:
            return make_response(jsonify(code=401, msg="Unauthorized", data={
                "hello": f"Hello! This is the dashboard service of the Data Integration Center. Today is  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            }), 401)
        return make_response(jsonify(code=200, msg="ok", data={
            "hello": f"Hello! This is the dashboard service of the Data Integration Center. Today is  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        }))

class MapItemStatusRatioResource(Resource):

    def __get_day(self):
        # Calculate the start date
        start_date = datetime.now() - timedelta(days=30)

        pipeline = [
            {
                "$match": {
                    "create_at": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": {
                            "$dateToString": {"format": "%Y-%m-%d", "date": "$create_at"}
                        },
                        "status": "$status"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"_id.date": 1}
            }
        ]

        results = MapItem.objects().aggregate(*pipeline)
        print(results)
        data = [{
            'year': result['_id']['date'],
            'value': result['count'],
            'type': result['_id']['status']
        }for result in results]
        return make_response(jsonify(code=200, msg="ok", data=data),200)


    def get(self):
        
            

        try:
            in_schema = GetMapItemStatusRatioSchema().load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        range = in_schema['range']

        if range == 'day':
            return self.__get_day()
        elif range == 'week':
            pass
        elif range == 'month':
            pass
        
        import random
        
        data = []
        years = [1995,1996,1997,1998,1999,2000,2001]
        for year in years:
            data.append({'year':str(year),'value':random.randint(1,10),'type':'success'})
        for year in years:
            data.append({'year':str(year),'value':random.randint(1,10),'type':'failed'})

        return make_response(jsonify(code=200, msg="ok", data=data))

    
class PredictSingleResource(Resource):

    def post(self):

        data = request.get_json()
        if 'text' not in data:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        text = data['text']
        map_url = app.config['MAP_SERVICE_URL']
        res = requests.post(f'{map_url}/predict', json={'texts': [text]})

        if res.status_code != 200:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

        return make_response(jsonify(code=200, msg="ok", data=res.json()['data']), 200)
