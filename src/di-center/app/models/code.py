from mongoengine import Document, StringField, IntField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField, BooleanField
from .document import DIDocument as Document

class CodeSystem(Document):
    name = StringField(required=True)
    description = StringField(required=False, default='')
    create_by = ObjectIdField(required=True)
    version = StringField(unique=True,required=True)
    deleted = BooleanField(default=False)

class Concept(Document):
    name = StringField(unique=True, required=True)

class Tag(Document):
    name = StringField(unique=True,required=True)
    source = StringField(required=True, choice=('official', 'user'))

    meta = {
        'indexes': [
            {'fields': ['name', 'source'], 'unique': True}
        ]
    }

class ConceptGroup(Document):
    name = StringField(unique=True,required=True)

class ConceptVersion(Document):
    code_system = ReferenceField(CodeSystem, required=True)
    concept = ReferenceField(Concept, required=True)
    alias = StringField(required=False, default='')         # latest user alias of the category
    tags = ListField(ReferenceField(Tag), required=False)
    group = ReferenceField(ConceptGroup, required=True)
