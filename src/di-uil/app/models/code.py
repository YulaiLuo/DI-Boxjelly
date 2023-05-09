from mongoengine import Document, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from datetime import datetime
from .document import DIDocument

class ConceptGroup(DIDocument):
    name = StringField(required=True)                               # group name
    code_system_id = ObjectIdField(required=True)                              # id of the UIL list
    create_by = ObjectIdField(required=False)                       # creator id

class Concept(DIDocument):
    code_system_id = ObjectIdField(required=True)                              # id of the code system
    group_id = ObjectIdField(required=False)                              # id of the concept group
    parent_concept_id = ObjectIdField(required=False, default=None)                              # id of the parent concept
    child_concept_id = ObjectIdField(required=False, default=None)      
    # tag_id = ListField(ObjectIdField(), required=False, default=[])

    name = StringField(unique=True, required=True)                              # the indication name in this version
    description = StringField(required=False, default='')                        # user alias of the category in this version
    
    create_by = ObjectIdField(required=True)                        # creator id

class ConceptMap(DIDocument):
    relation = StringField(required=False, default='isRelated')                               # name of the version
    concept_id_1 = ObjectIdField(required=True)                              # id of the code system
    concept_id_2 = ObjectIdField(required=True)                              # id of the concept group

class CodeSystem(DIDocument):
    team_id = ObjectIdField(required=True)

    name = StringField(required=True)                               # name of the version
    description = StringField(required=False)                       # description of the version

    create_by = ObjectIdField(required=True)  # creator id
