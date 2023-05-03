from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

class FileField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        return value

class CreateMapTaskInputSchema(Schema):
    # user_team_id = fields.String(required=True)
    file = FileField(required=True)

    @validates('file')
    def validate_file(self, file):
        if not allowed_file(file.filename):
            raise ValidationError("File type not allowed. Allowed file types: csv, xlsx, xls")
        
class DeleteMapTaskInputSchema(Schema):
    id = fields.String(required=True)