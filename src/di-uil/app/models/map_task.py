from datetime import datetime

from mongoengine import Document, StringField, IntField, DateTimeField, ObjectIdField, BooleanField

class MapTask(Document):
    
    status = StringField(default='pending')                    # 0: pending, 1: success, 2: rejected, 3: failed
    num = IntField(required=True, min_value=1)                           # number of items to map in the task
    create_by = ObjectIdField(required=True)
    create_at = DateTimeField(default=datetime.utcnow)
    update_at = DateTimeField(default=datetime.utcnow)
    deleted = BooleanField(default=False)
    file_name = StringField(required=True)
    
    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(MapTask, self).save(*args, **kwargs)
