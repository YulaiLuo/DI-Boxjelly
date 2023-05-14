from mongoengine import Document, ReferenceField, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
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

class User(DIDocument):
    # avatar = StringField(required=True)                               # group name
    username = StringField(unique=True,required=True)                               # group name
    email = StringField(unique=True,required=True)                               # group name
    password = StringField(required=True)                               # group name
    first_name = StringField(required=True)                               # group name
    last_name = StringField(required=True)                               # group name
    nickname = StringField(required=False)                               # group name
    gender = StringField(required=False,choices=('male','female','other'))                               # gender
    
class Team(DIDocument):
    name = StringField(required=True)                               # group name
    create_by = ReferenceField(User,required=True)                       # creator id

class UserTeam(DIDocument):
    user_id = ReferenceField(User,default=None)    # user id
    team_id = ReferenceField(Team,required=True)    # team id
    role = StringField(default='normal',choices=('owner', 'normal'))
    invite_by = ReferenceField(User,required=True)    # user id
    invite_email = StringField(required=True)   # invited email
   
    status = StringField(default='pending',choices=('active','absent','pending'))
    join_time = DateTimeField(required=False)    # join time
    last_login_time = DateTimeField(default=datetime.utcnow)    # last login time
