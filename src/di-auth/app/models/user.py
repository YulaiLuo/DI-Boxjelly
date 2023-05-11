from mongoengine import Document, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from .document import DIDocument

class User(DIDocument):
    # avatar = StringField(required=True)                               # group name
    username = StringField(unique=True,required=True)                               # group name
    first_name = StringField(required=True)                               # group name
    last_name = StringField(required=True)                               # group name
    email = StringField(required=True)                               # group name
    nickname = StringField(required=False)                               # group name
    gender = StringField(required=False)                               # gender
    password = StringField(required=True)                               # group name

class UserTeam(DIDocument):
    user_id = ObjectIdField(required=True)      # user id
    team_id = ObjectIdField(required=True)      # team id
    role = StringField(required=True)           # 'owner', 'normal'
    status = StringField(default='active')      # 'active','leave','pending'
    invite_by = ObjectIdField(required=True)                       # invited by who
