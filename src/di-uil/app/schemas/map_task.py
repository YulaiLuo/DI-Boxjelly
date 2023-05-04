from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
from .helper import FileField, allowed_file
import os

class CreateMapTaskInputSchema(Schema):
    # user_team_id = fields.String(required=True)
    file = FileField(required=True)
    create_by = fields.String(required=True)

    @validates('file')
    def validate_file(self, file):
        if not allowed_file(file.filename, app.config['MAP_TASK_ALLOWED_EXTENSIONS']):
            raise ValidationError("FILE_NOT_ALLOWED")
        
class DeleteMapTaskInputSchema(Schema):
    id = fields.String(required=True)

class GetMapTaskInputSchema(Schema):
    page = fields.Integer(required=False,default=1, min_value=1)
    size = fields.Integer(required=False,default=20, min_value=10)

class GetAllMapTaskInputSchema(Schema):
    page = fields.Integer(required=False,default=1, min_value=1)
    size = fields.Integer(required=False,default=20, min_value=10)
