from mongoengine import Document, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from datetime import datetime

class MappedInfo(EmbeddedDocument):
    system = StringField()                  # code system: UIL, Snomed CT, ...
    source = StringField()                  # mapper name: Medcat, Self, ...
    mappedCode = StringField()              # id of the mapped item
    curatedCode = StringField()             # curated code
    confidenceScore = FloatField()          # confidence score of the mapping
    status = IntField()                     # 0: success, 1: failed, 2: reviewed

class MapItem(Document):

    task_id = ObjectIdField(required=True)                       # id of the map task
    text = StringField(required=True, index=True)                        # raw text of the clinical text  
    mapped_info = ListField(EmbeddedDocumentField(MappedInfo))   # mapped information
    createAt = DateTimeField(default=datetime.utcnow)
    updateAt = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updateAt = datetime.utcnow()
        super(MapItem, self).save(*args, **kwargs)
