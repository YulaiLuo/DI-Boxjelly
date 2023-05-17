from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, FloatField, ReferenceField, StringField, IntField, ListField, ObjectIdField, BooleanField
from .document import DIDocument
from .code import CodeSystem, Concept, ConceptGroup

class MapTask(DIDocument):
    team_id = ObjectIdField(required=True)
    board_id = ObjectIdField(required=True)                              # id of the board

    num = IntField(required=True, min_value=1)                           # number of items to map in the task
    status = StringField(default='pending')            # pending, success, rejected, failed
    file_name = StringField(required=True)

    create_by = ObjectIdField(required=True)
    deleted = BooleanField(default=False)

class MapItem(DIDocument):
    # From creating task
    task_id = ObjectIdField(required=True)                          # id of the map task
    text = StringField(required=True, index=True)                   # raw text of the clinical text      

    # From mapper
    confidence = FloatField()                                       # confidence score of the mapping
    mapped_concept = ReferenceField(Concept, required=False)               # concept id
    status = StringField(default='fail', choices=('success', 'fail', 'reviewed'))                                          # success, fail, reviewed
    

    # From curator
    curated_concept = ReferenceField(Concept, required=False)       # curated concept id

class TaskBoard(DIDocument):
    team_id =  ObjectIdField(required=True)                         # id of the team
    name = StringField(required=True)                               # name of the version
    description = StringField(required=False)                       # description of the version
    deleted = BooleanField(default=False)                           # soft delete