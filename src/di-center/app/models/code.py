from mongoengine import Document, StringField, IntField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField, DateTimeField, FloatField, ListField, ObjectIdField
from .document import DIDocument as Document

class CodeSystem(Document):
    team_id = ObjectIdField(required=True)
    name = StringField(required=True)                               
    description = StringField(required=False)                      
    create_by = ObjectIdField(required=True)  # creator id

class ConceptVersion(Document):
    name = StringField(required=True)           # version name                         
    code_system = ReferenceField(CodeSystem, required=True)         
    concept = ReferenceField('Concept', required=True)               

class ConceptGroup(Document):
    name = StringField(required=True)                               
    code_system = ReferenceField(CodeSystem, required=True)       
    create_by = ObjectIdField(required=False)                  

class Tag(Document):
    name = StringField(required=True)                            

class Concept(Document):
    name = StringField(unique=True, required=True)
    group = ReferenceField(ConceptGroup, required=True)
    alias = StringField(required=False, default='')
    tags = ListField(ReferenceField(Tag), required=False)
    my_tags = ListField(ReferenceField(Tag), required=False)

    # code_system = ReferenceField(CodeSystem, required=True)         
    # parent_concept = ReferenceField('self', required=False)         
    # child_concept = ReferenceField('self', required=False)           
    # create_by = ObjectIdField(required=True)                        

    description = StringField(required=False, default='')          
    
