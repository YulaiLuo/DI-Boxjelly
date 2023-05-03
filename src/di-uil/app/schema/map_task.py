from marshmallow import Schema, fields, ValidationError, validate

ALLOWED_EXTENSIONS = {'csv','xlsx','xls'}

def validate_file(file):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FileField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        return value

class CreateMapTaskInputSchema(Schema):
    user_team_id = fields.String(required=True)
    file = FileField(required=True, validate=validate_file)

class CreateMapTaskOutputSchema(Schema):

    

    pass