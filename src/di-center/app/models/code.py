from mongoengine import Document, StringField, IntField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from .document import DIDocument as Document

class CodeSystem(Document):
    team_id = ObjectIdField(required=True)
    name = StringField(required=True)                               # name of the version
    description = StringField(required=False)                       # description of the version
    # version = StringField(required=True)                          # version of the code system
    create_by = ObjectIdField(required=True)  # creator id

class ConceptGroup(Document):
    name = StringField(required=True)                               # group name
    code_system = ReferenceField(CodeSystem, required=True)     # id of the UIL list
    create_by = ObjectIdField(required=False)                       # creator id

class Concept(Document):
    code_system = ReferenceField(CodeSystem, required=True)     # id of the UIL list
    group_id = ObjectIdField(required=False)                        # id of the concept group
    
    parent_concept = ReferenceField('self', required=True)     # id of the UIL list
    child_concept = ReferenceField('self', required=True)     # id of the UIL list

    name = StringField(unique=True, required=True)                  # the indication name in this version
    description = StringField(required=False, default='')           # user alias of the category in this version
    
    create_by = ObjectIdField(required=True)                        # creator id
