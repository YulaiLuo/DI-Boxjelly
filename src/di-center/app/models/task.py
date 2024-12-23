from datetime import datetime
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, DictField, FloatField, ReferenceField, StringField, IntField, ListField, ObjectIdField, BooleanField
from .document import DIDocument as Document
from .code import CodeSystem, Concept, ConceptGroup, ConceptVersion

class Mapper(Document):
    name = StringField(required=True, unique=True)
    description = StringField(required=True)

class TaskBoard(Document):
    team_id =  ObjectIdField(required=True)                         # id of the team
    name = StringField(required=True)                               # name of the version
    description = StringField(required=False)                       # description of the version
    deleted = BooleanField(default=False)                           # soft delete

class MapTask(Document):
    team_id = ObjectIdField(required=True)
    board = ReferenceField(TaskBoard,required=True)                              # id of the board
    mapper_name = ReferenceField(Mapper, required=True)                   # id of the mapper

    num = IntField(required=True, min_value=1)                           # number of items to map in the task
    status = StringField(default='pending')            # pending, success, rejected, failed
    file_name = StringField(required=True)

    create_by = ObjectIdField(required=True)
    deleted = BooleanField(default=False)

class MapItem(Document):
    # From creating task
    task = ReferenceField(MapTask, index=True, required=True)                # id of the task
    text = StringField(required=True, index=True)                   # raw text of the clinical text      

    # From mapper
    accuracy = FloatField()                                       # confidence score of the mapping
    mapped_concept = StringField()                   # mapped concept id
    status = StringField(default='fail', index=True, choices=('success', 'fail', 'reviewed'))                                          # success, fail, reviewed
    ontology = StringField(index=True)                         # ontology of the concept
    extra = DictField(default={})

    # From curator
    curated_concept = ReferenceField(ConceptVersion, required=False)       # curated concept id
    deleted = BooleanField(default=False)                           # soft delete
