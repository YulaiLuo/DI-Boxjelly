from flask_restful import Resource
from flask import jsonify, request, make_response
from app.models import MapTask, MapItem
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
import math, threading, requests

class GetMapTaskBoardInputSchema(Schema):
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)
    page = fields.Integer(required=False,default=1, min_value=1)
    size = fields.Integer(required=False,default=20, min_value=10)

class PostMapTaskBoardInputSchema(Schema):
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)
    file = fields.Field(required=True)
   
    def _allowed_file(self, filename, allowed_extensions):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @validates('file')
    def validate_file(self, file):
        if not self._allowed_file(file.filename, app.config['MAP_TASK_ALLOWED_EXTENSIONS']):
            raise ValidationError("FILE_NOT_ALLOWED")

class MapTaskBoardResource(Resource):
    """
    Resource for the map task list
    """

    def get(self, board_id):
        """
        Check the permission and get the map task list of a workspace

        Returns:
            Response: tasks list
        """
        in_schema = GetMapTaskBoardInputSchema()
        
        try:
            # TODO: check the permission
            # user_id = request.headers.get('user_id')
            # team_id = team_id

            in_schema = in_schema.load(request.args)

            page = in_schema['page']
            size = in_schema['size']
            map_tasks = MapTask.objects(board_id=board_id,deleted=False).all().skip((page-1)*size).limit(size)
            
            # Convert the tasks to a list of dictionaries
            # TODO: search pipeline
            data = {
                'page': page,
                'size': size,
                'page_num': math.ceil(len(map_tasks)/size),
                'tasks':[{
                    "id": str(task.id),
                    "status": task.status,
                    "num": task.num,
                    "create_by": str(task.create_by),
                    "create_at": task.create_at,
                    "update_at": task.update_at
                }
                for task in map_tasks]
            }
            
            response = jsonify(code=200, msg="ok", data=data)
            response.status_code = 200
            return response
        
        except ValidationError as err:
            response = jsonify(code=400, err="INVALID_INPUT")
            response.status_code = 400
            return response
            
        except Exception as err:
            print(err)
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response
        
      # Thread function to process the mapping task
    def map_items(self, map_url ,new_map_task, texts):

        # Invoke the map api to convert the raw text to snomed ct
        # res = requests.get('http://localhost:8003/map/translate', json={'texts': texts}).json()
        res = requests.get(f'{map_url}/map/translate', json={'texts': texts}).json()
        
        if res['msg']!='ok':
            new_map_task.status = 'fail'
            new_map_task.save()
            return 
        
        # TODO: add the UIL version to the map task
        # uil_categories = UILCategory.objects.all()
        # for i in range(len(texts)):
        #    mapped_info = res['data'][str(i)]
        #    for item in mapped_info:
        #       for category in uil_categories:
        #          if item['sct_code'] in category.snomed_ct.sct_code:
        #             item['mapped_uil_id'] = category.id
        #             item['source'] = 'UIL'
        #             item['status'] = 'success'
        #             break
                
        # Create map items
        new_map_items = [
                            MapItem(task_id = new_map_task.id,
                            text=texts[i],
                            status='success' if len(res['data'][str(i)])>0 else 'fail',
                            mapped_info=res['data'][str(i)]
                            ) for i in range(len(texts))
                        ]

        # Save
        new_map_task.status = 'success'
        new_map_task.save()
        MapItem.objects.insert(new_map_items)

    def post(self):
        """
        Create a new map task

        Returns:
            _type_: _description_
        """

        # Create schema new map task API input schema
        in_schema = PostMapTaskBoardInputSchema()

        # The data can come from file, form and ...etc
        data = {}
        data.update(request.files)
        data.update(request.form)

        try: 
            # load the data
            in_schema = in_schema.load(data)
            texts = in_schema['file'].readlines()
            texts = [text.decode('utf-8').strip() for text in texts]
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"),400)
        
        try:
            # user_id = request.headers.get('user_id')
            user_id = '60c879e72cb0e6f96d6b0f65'

            new_map_task = MapTask(
                num = len(texts),
                team_id = in_schema['team_id'],
                board_id = in_schema['board_id'],
                create_by = ObjectId(user_id)
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

        except Exception as err:
            print(err)
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response