from mongoengine import Document, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from datetime import datetime

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

class MapItem(Document):

    task_id = ObjectIdField(required=True)                       # id of the map task
    text = StringField(required=True, index=True)                        # raw text of the clinical text  
    mapped_info = ListField(EmbeddedDocumentField(MappedInfo))   # mapped information
    status = StringField()                  # success, fail, review
    create_at = DateTimeField(default=datetime.utcnow)
    update_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updateAt = datetime.utcnow()
        super(MapItem, self).save(*args, **kwargs)
