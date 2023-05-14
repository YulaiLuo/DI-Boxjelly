from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, FloatField, StringField, IntField, ListField, ObjectIdField, BooleanField

from .document import DIDocument

class MapTask(DIDocument):
    team_id = ObjectIdField(required=True)
    board_id = ObjectIdField(required=True)                              # id of the board

    num = IntField(required=True, min_value=1)                           # number of items to map in the task
    status = StringField(default='pending')            # pending, success, rejected, failed
    file_name = StringField(required=True)

    create_by = ObjectIdField(required=True)
    deleted = BooleanField(default=False)

class MappedInfo(EmbeddedDocument):
    start_index = IntField()                # start index of the mapped item
    end_index = IntField()                  # end index of the mapped item
    sct_code = StringField()                # id of the mapped item
    sct_term = StringField()                # term of the mapped item
    type = StringField()                    # semantic tag of the mapped item
    similarity = FloatField()               # similarity score of the mapping
    confidence = FloatField()          # confidence score of the mapping
    status = StringField()
    source = StringField()                  # mapper name: Medcat, Self, ...
    mapped_uil_id = ObjectIdField()         # mapped code
    curated_uil_id = ObjectIdField()        # curated code

class MapItem(DIDocument):

    task_id = ObjectIdField(required=True)                       # id of the map task
    text = StringField(required=True, index=True)                        # raw text of the clinical text  
    mapped_info = ListField(EmbeddedDocumentField(MappedInfo))   # mapped information
    status = StringField()                  # success, fail, review

class TaskBoard(DIDocument):
    team_id =  ObjectIdField(required=True)                       # id of the team
    name = StringField(required=True)                               # name of the version
    description = StringField(required=False)                       # description of the version
