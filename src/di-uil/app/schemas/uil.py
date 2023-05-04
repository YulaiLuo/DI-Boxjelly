from marshmallow import Schema, fields, ValidationError, validates
from flask import current_app as app
from .helper import FileField, allowed_file
import os

class CreateUILCategoryInputSchema(Schema):

    indication = fields.String(required=True)                               # latest name of the category
    user_alias = fields.String(required=False)                               # latest user alias of the category
    tags = fields.List(fields.String(), required=False)                       # latest tags of the category
    group_id = fields.String(required=False)                               # id of the group
    create_by = fields.String(required=True)                      # creator id

class CreateUILInputSchema(Schema):
    version = fields.String(required=True)                            # version number
    description = fields.String(required=False)                       # description of the version
    create_by = fields.String(required=False)                        # creator id

    # @validates('file')
    # def validate_file(self, file):
    #     if not allowed_file(file.filename, app.config['NEW_UIL_ALLOWED_EXTENSIONS']):
    #             raise ValidationError("FILE_NOT_ALLOWED")

class CreateUILGroupInputSchema(Schema):
    name = fields.String(required=True)                            # version number
    create_by = fields.String(required=True) 
    
