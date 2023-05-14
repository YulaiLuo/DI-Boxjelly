from flask_restful import Resource
from flask import jsonify, request, make_response
from mongoengine.errors import DoesNotExist
from app.models import MapTask, MapItem
from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
import math
import threading
import requests
import codecs
import csv
from io import StringIO
from bson import ObjectId


class DeleteMapTaskInputSchema(Schema):
    task_id = fields.String(required=True)
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)


class GetMapTaskInputSchema(Schema):
    task_id = fields.String(required=True)
    team_id = fields.String(required=True)
    board_id = fields.String(required=True)
    page = fields.Integer(required=False, default=1, min_value=1)
    size = fields.Integer(required=False, default=20, min_value=10)


class PostMapTaskInputSchema(Schema):
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


class MapTaskResource(Resource):
    """
    The MapTaskResource class is used to handle the request of map task.
    """
    # Get map task detail by id

    def get(self):

        try:
            in_schema = GetMapTaskInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            print(err)
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 404)

        try:
            task_id = in_schema['task_id']
            map_task = MapTask.objects(
                id=ObjectId(task_id), deleted=False).first()
            if not map_task:
                return make_response(jsonify(code=404, err="MAP_TASK_NOT_FOUND"), 404)

            page = in_schema['page']  # min_value 1
            size = in_schema['size']  # min_value 10
            map_items = MapItem.objects(task_id=ObjectId(
                task_id)).skip((page-1)*size).limit(size)

            # items = [{'text':item.text, 'status':item.status,'mapped_info':item.mapped_info} for item in map_items]
            items = [{'text': map_item['text'], 'status': map_item['status'], 'mapped_info': map_item['mapped_info']}
                     for map_item in (mi.to_mongo().to_dict() for mi in map_items)]

            data = {
                'id': str(map_task.id),       # task id
                'status': map_task.status,
                'items': items,
                'page': page,
                'size': size,
                'page_num': math.ceil(map_task.num/size),
                'file_name': map_task.file_name
            }

            response = jsonify(code=200, msg="ok", data=data)
            response.status_code = 200
            return response

        except Exception as err:
            print(err)
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response

    def delete(self):
        """
        Soft delete a map task in the database by changing the deleted as True

        Args:
            task_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            in_schema = DeleteMapTaskInputSchema()
            in_schema = in_schema.load(request.args)
        except ValidationError as err:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 404)

        try:
            # TODO: Check if the task is permitted to be deleted by this user

            # TODO: Check if the task is deleted

            # Change the deleted field as deleted
            MapTask.objects(id=ObjectId(
                in_schema['task_id'])).update_one(deleted=True)

            response = jsonify(code=200, msg="ok")
            response.status_code = 200
            return response

        except ValidationError as err:
            print(err)
            response = jsonify(code=400, err="INVALID_INPUT")
            response.status_code = 400
            return response

        except Exception as err:
            response = jsonify(code=500, err="INTERNAL_SERVER_ERROR")
            response.status_code = 500
            return response

    # Thread function to process the mapping task
    def map_items(self, map_url, new_map_task, texts):
        # Invoke the map api to convert the raw text to snomed ct
        res = requests.post(f'{map_url}/map/translate',
                            json={'texts': texts}).json()

        if res['msg'] != 'ok':
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
            MapItem(task_id=ObjectId(new_map_task.id),
                    text=texts[i],
                    status='success' if len(
                        res['data'][str(i)]) > 0 else 'fail',
                    mapped_info=res['data'][str(i)]
                    ) for i in range(len(texts))
        ]
        # Save
        new_map_task.status = 'success'
        new_map_task.save()
        MapItem.objects.insert(new_map_items)

    def post(self):

        # Create schema new map task API input schema
        in_schema = PostMapTaskInputSchema()

        # The data can come from file, form and ...etc
        data = {}
        data.update(request.files)
        data.update(request.form)

        try:
            # load the data
            in_schema = in_schema.load(data)
            file = in_schema['file']
            file_ext = file.filename.split('.')[-1].lower()

            texts = []

            if file_ext == 'txt':
                lines = file.readlines()
                lines = [line.decode('utf-8').strip() for line in lines]
                if lines and codecs.BOM_UTF8.decode('utf-8') in lines[0]:
                    lines[0] = lines[0].replace(
                        codecs.BOM_UTF8.decode('utf-8'), '')
                for line in lines:
                    # Split on tab character and take the second part as your text
                    parts = line.split('\t')
                    if len(parts) > 1:
                        texts.append(parts[1])
                    else:
                        texts.append(parts[0])

            elif file_ext == 'csv':
                file_content = file.read().decode('utf-8')
                if codecs.BOM_UTF8.decode('utf-8') in file_content:
                    file_content = file_content.replace(
                        codecs.BOM_UTF8.decode('utf-8'), '')
                text_stream = StringIO(file_content)
                reader = csv.reader(text_stream, delimiter=',', quotechar='"')
                # next(reader)  # Skip the header (if there is one)
                for row in reader:
                    # Assuming the text data is in the first column of the CSV
                    texts.append(row[0])
            else:
                print("Invalid file format. Please upload a TXT or CSV file.")

            # TODO: Get user id from header
            # user_id = request.headers['user_id']
            user_id = '60c879e72cb0e6f96d6b0f65'
            new_map_task = MapTask(
                num=len(texts),
                create_by=ObjectId(user_id),
                # created_by = request.user_team_id
                file_name=file.filename,
                team_id=ObjectId(in_schema['team_id']),
                board_id=ObjectId(in_schema['board_id'])
            )

            # Save map task
            new_map_task.save()

            # Create a new thread to process the mapping task
            map_url = app.config['MAP_SERVICE_URL']
            thread = threading.Thread(
                target=self.map_items, args=(map_url, new_map_task, texts))
            thread.start()

            response = jsonify(code=200,
                               msg="ok",
                               data={
                                   'id': str(new_map_task.id),
                                   'status': new_map_task.status
                               })
            response.status_code = 200
            return response

        except ValidationError as err:
            print(err)
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        except Exception as err:
            print(err)
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
