from mongoengine import Document, StringField, IntField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from datetime import datetime

class DIDocument(Document):

    create_at = DateTimeField(default=datetime.utcnow)              # create time
    update_at = DateTimeField(default=datetime.utcnow)              # update time

    # set meta allow_inheritance as true
    meta = {'allow_inheritance': True, 
            "abstract": True}

    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(DIDocument, self).save(*args, **kwargs)

class MedcatConceptMap(DIDocument):
    
    # From Medcat
    accuracy = FloatField()
    sct_code = StringField(unique=True, sparse=True, index=True)
    sct_term = StringField()
    sct_pretty_name = StringField()
    sct_status = StringField()
    sct_status_confidence = FloatField()
    sct_types = ListField(StringField())
    sct_types_ids = ListField(StringField())

    status = StringField(required=True, choices=('fail','success','reviewed'))

    # From curating
    # curated_uil_id = ObjectIdField(required=False)
    curated_uil_name = StringField(required=False,default='')
    curated_uil_group = StringField(required=False,default='')

class MedcatTextMap(DIDocument):

    # Raw clinical text
    text = StringField(required=True, index=True, unique=True)
    map = ReferenceField(MedcatConceptMap, required=False)
