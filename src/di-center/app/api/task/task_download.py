from datetime import datetime
from collections import Counter
from flask_restful import Resource
from flask import jsonify, make_response, Response, request
from app.models import MapItem, MapTask
import csv
import io
from bson import ObjectId
from marshmallow import Schema, fields, ValidationError, validates
import traceback


class GetDownloadMapTaskInputSchema(Schema):
    team_id = fields.String(required=True)
    task_id = fields.String(required=True)


class DownloadMapTaskResource(Resource):

    def export_map_task_to_csv(self, map_task, map_items):

        csv_data = io.StringIO()
        csv_writer = csv.writer(csv_data, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Get the meta data of map task
        total_num = map_task.num
        creation_date = map_task.create_at

        # Get the status count of map items
        status_ctr = Counter([item.status for item in map_items])
        success_count = status_ctr['success']
        fail_count = status_ctr['fail']
        reviewed_count = status_ctr['reviewed']

        # Meta Data
        csv_writer.writerow(['Total Number', 'Success Count',
                            'Failure Count', 'Review Count', 'Creation Date'])
        csv_writer.writerow(
            [total_num, success_count, fail_count, reviewed_count, creation_date])

        # Add space between meta data and map items
        csv_writer.writerow([])

        # Map Items
        csv_writer.writerow(['Text', 'Output', 'Confidence',
                            'Source', 'Curated UIL', 'Status'])
        for item in map_items:
            status = item['status']
            if status == 'success':
                if item['extra'].get('2'):
                    csv_writer.writerow([item['text'],
                                        item['mapped_concept'],
                                        item['accuracy'] if (item['ontology'] != 'UIL') | (
                                            item['extra']['2']['value'] == 'UIL') else '-',
                                        item['ontology'],
                                        '-' if item['curated_concept'] == None else item['curated_concept']['concept']['name'],
                                         status])
                else:
                    csv_writer.writerow([item['text'],
                                        item['mapped_concept'],
                                        item['accuracy'] if item['ontology'] != 'UIL' else '-',
                                        item['ontology'],
                                        '-' if item['curated_concept'] == None else item['curated_concept']['concept']['name'],
                                         status])
            elif status == 'reviewed':
                csv_writer.writerow([item['text'],
                                     item['mapped_concept'],
                                     item['accuracy'] if item['ontology'] != 'UIL' else '-',
                                     item['ontology'],
                                     '-' if item['curated_concept'] == None else item['curated_concept']['concept']['name'],
                                     status])
            else:
                csv_writer.writerow([item['text'],
                                     '-',
                                     '-',
                                     '-',
                                     '-',
                                     item['status']])

        return csv_data.getvalue().encode('utf-8')

    def get(self):
        """Download the map task result
        """
        try:
            in_schema = GetDownloadMapTaskInputSchema()
            in_schema = in_schema.load(request.args)
        except:
            return make_response(jsonify(code=400, err="INVALID_INPUT"), 400)

        try:
            task_id = in_schema['task_id']
            map_task = MapTask.objects(
                id=ObjectId(task_id), deleted=False).first()
            if not map_task:
                return make_response(jsonify(code=404, err="MAP_TASK_NOT_FOUND"), 404)

            map_items = MapItem.objects(task=ObjectId(task_id)).all()
            if not map_items:
                return make_response(jsonify(code=404, err="MAP_ITEM_NOT_FOUND"), 404)

            csv_data = self.export_map_task_to_csv(map_task, map_items)

            response = Response(csv_data, content_type='text/csv, utf-8')
            response.headers.set('Content-Disposition', 'attachment',
                                 filename=f"map_task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            return response

        except Exception as err:
            print(err)
            print(traceback.print_exc())
            return make_response(jsonify(code=500, err="INTERNAL_SERVER_ERROR"), 500)
