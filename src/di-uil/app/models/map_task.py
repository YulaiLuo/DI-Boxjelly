from datetime import datetime


from mongoengine import Document, StringField, IntField, DateTimeField, ObjectIdField

class MapTask(Document):
    
    status = IntField(default=0)                    # 0: pending, 1: success, 2: rejected, 3: failed
    item_num = IntField()                           # number of items to map in the task
    create_by = StringField()                     # user_team_id
    create_at = DateTimeField(default=datetime.utcnow)
    update_at = DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(MapTask, self).save(*args, **kwargs)
