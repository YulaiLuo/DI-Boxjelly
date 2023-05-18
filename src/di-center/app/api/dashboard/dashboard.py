from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import ConceptGroup, Concept, CodeSystem, MapItem, MapTask
from flask import current_app as app
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta, MO
from mongoengine import Q
import requests

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
            "title": f"Total Tasks: {task_count}",
            "total_number": f"This week: {this_week_count}",
            "delta": f"{'+' if delta>0 else '1'}{delta} since last week",
            "percent": delta/last_week_count*100 if last_week_count > 0 else 0
        }))

class TopMiddleResource(Resource):

    def get(self):

        # Calculate the start of this week and the start of the last week
        start_of_this_week, start_of_last_week = get_start_of_weeks()

        # Get all undeleted MapTask ids
        undeleted_task_ids = [task.id for task in MapTask.objects(deleted=False)]

        this_week_count = MapItem.objects(Q(task__in=undeleted_task_ids) & Q(create_at__gte=start_of_this_week)).count()
        last_week_count = MapItem.objects(Q(task__in=undeleted_task_ids) & Q(create_at__gte=start_of_last_week) & Q(create_at__lt=start_of_this_week)).count()

        delta = this_week_count - last_week_count
        total_count = MapItem.objects(task__in=undeleted_task_ids).count()

        return make_response(jsonify(code=200, msg="ok", data={
            "title": f"Total texts: {total_count}",
            "total_number": f"This week: {this_week_count}",
            "delta": f"{'+' if delta>0 else '1'}{delta} since last week",
            "percent": delta/last_week_count*100 if last_week_count > 0 else 0
        }))

class TopRightResource(Resource):

    def get(self):

        # Calculate the start of this week and the start of the last week
        start_of_this_week, start_of_last_week = get_start_of_weeks()

        this_week_count = MapItem.objects(status='reviewed', create_at__gte=start_of_this_week).count()
        last_week_count = MapItem.objects(status='reviewed', create_at__gte=start_of_last_week, create_at__lt=start_of_this_week).count()
        
        delta = this_week_count - last_week_count
        total_count = MapItem.objects(status='reviewed').count()

        return make_response(jsonify(code=200, msg="ok", data={
            "title": f"Total curated: {total_count}",
            "total_number": f"This week: {this_week_count}",
            "delta": f"{'+' if delta>0 else '1'}{delta} since last week",
            "percent": delta/last_week_count*100 if last_week_count > 0 else 0
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

    
class PredictSingleResource(Resource):

    def post(self):

        data = request.get_json()
        if 'text' not in data:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)
        
        text = data['text']
        map_url = app.config['MAP_SERVICE_URL']
        res = requests.post(f'{map_url}/map/predict', json={'texts': [text]})

        if res.status_code != 200:
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)

        return make_response(jsonify(code=200, msg="ok", data=res.json()['data']), 200)
