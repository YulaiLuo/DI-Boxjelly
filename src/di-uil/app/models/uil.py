from mongoengine import Document, StringField, IntField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from datetime import datetime

class SnomedCT(EmbeddedDocument):
    sct_code = StringField(required=True)
    sct_term = StringField(required=True)

class UILGroup(Document):
    name = StringField(required=True)                               # group name
    uil_version = StringField(required=True)                           # id of the UIL version
    create_at = DateTimeField(default=datetime.utcnow)              # create time
    update_at = DateTimeField(default=datetime.utcnow)              # update time
    create_by = ObjectIdField(required=False)                       # creator id
    deleted = IntField(default=0)

    meta = {
        'collection': 'uil_group', # The default collection name is u_i_l_group, so change it to uil_group
        'unique_with': ['name', 'uil_version']
    }

    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(UILGroup, self).save(*args, **kwargs)

class UILCategory(Document):
    indication = StringField(unique=True, required=True)                              # the indication name in this version
    user_alias = StringField(required=False)                        # user alias of the category in this version
    tags = ListField(StringField(), required=False)                 # tags of the category in this version
    snomed_ct = EmbeddedDocumentField(SnomedCT, required=False)     # snomed ct info of the category in this version
    group_id = ObjectIdField(required=False)                            # id of the UIL group
    uil_id = ObjectIdField(required=True)                              # id of the UIL list
    create_at = DateTimeField(default=datetime.utcnow)              # create time
    update_at = DateTimeField(default=datetime.utcnow)              # update time
    create_by = ObjectIdField(required=True)                        # creator id

    meta = {
        'collection': 'uil_category' # The default collection name is u_i_l, so change it to uil
    }

    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(UILCategory, self).save(*args, **kwargs)

class UIL(Document):
    version = StringField(required=True, unique=True)                              # version number  
    description = StringField(required=False)                       # description of the version
    create_at = DateTimeField(default=datetime.utcnow)              # create time
    update_at = DateTimeField(default=datetime.utcnow)              # update time
    create_by = ObjectIdField(required=True)                        # creator id

    meta = {
        'collection': 'uil' # The default collection name is u_i_l, so change it to uil
    }

    def save(self, *args, **kwargs):
        self.update_at = datetime.utcnow()
        super(UIL, self).save(*args, **kwargs)
