from mongoengine import Document, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from datetime import datetime
from .document import DIDocument

class Team(DIDocument):
    name = StringField(required=True)                               # group name
    create_by = ObjectIdField(required=False)                       # creator id
    status = StringField(default='valid')      # 'valid','leave'