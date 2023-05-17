from mongoengine import Document, DateTimeField
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