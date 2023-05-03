from mongoengine import (
    Document,
    ObjectIdField,
    StringField,
    IntField,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    ListField
)

from mongoengine import Document, StringField, IntField

class MappedInfo(EmbeddedDocument):
    system = StringField()                  # code system: UIL, Snomed CT, ...
    source = StringField()                  # mapper name: Medcat, Self, ...
    mappedCode = StringField()              # id of the mapped item
    curatedCode = StringField()             # curated code
    confidenceScore = FloatField()          # confidence score of the mapping
    status = IntField()                     # 0: success, 1: failed, 2: reviewed

class MapItem(Document):

    taskId = ObjectIdField(required=True)   
    rawText = StringField()
    mappedInfo = ListField(EmbeddedDocumentField(MappedInfo))
    createAt = DateTimeField()
    updateAt = DateTimeField()
    