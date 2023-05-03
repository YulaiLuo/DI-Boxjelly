from marshmallow import fields

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

class FileField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        return value