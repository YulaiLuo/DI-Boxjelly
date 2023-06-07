from mongoengine import Document, ReferenceField, StringField, DateTimeField, NotUniqueError
from datetime import datetime, timedelta
import uuid


class DIDocument(Document):

    create_at = DateTimeField(
        default=datetime.utcnow)              # create time
    update_at = DateTimeField(
        default=datetime.utcnow)              # update time

    # set meta allow_inheritance as true
    meta = {'allow_inheritance': True,
            "abstract": True}

    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(DIDocument, self).save(*args, **kwargs)


class User(DIDocument):
    avatar = StringField(required=False, default='default')
    username = StringField(unique=True, required=True)
    email = StringField(unique=True, required=True)
    password = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    nickname = StringField(required=False)
    gender = StringField(required=False, choices=(
        'Male', 'Female', 'Other'))


class Team(DIDocument):
    name = StringField(required=True)
    # create_by = ReferenceField(
    #     User, required=True)                       # creator id


class UserTeam(DIDocument):
    user_id = ReferenceField(User, default=None)    # user id
    team_id = ReferenceField(Team, required=True)    # team id
    role = StringField(default='memeber', choices=('owner', 'memeber'))
    invite_by = ReferenceField(User, required=True)    # user id

    status = StringField(default='active', choices=(
        'active', 'absent', 'pending'))
    join_time = DateTimeField(required=False)    # join time
    last_login_time = DateTimeField(
        default=datetime.utcnow)    # last login time


class Invitation(DIDocument):
    # unique token for the invitation
    invite_token = StringField(unique=True)
    team_id = ReferenceField(Team, required=True)  # team id
    # user id of the person who created the invitation
    invite_by = ReferenceField(User, required=True)
    expiry_date = DateTimeField(default=lambda: datetime.utcnow(
    ) + timedelta(days=1))  # expiry date for the invitation

    def save(self, *args, **kwargs):
        if not self.invite_token:
            self.invite_token = str(uuid.uuid4())

        try:
            return super(Invitation, self).save(*args, **kwargs)
        except NotUniqueError:
            self.invite_token = str(uuid.uuid4())
            return self.save(*args, **kwargs)


class BlackList(DIDocument):
    jti = StringField(required=True, index=True)
