from mongoengine import Document, StringField, EmailField,BooleanField,DateTimeField,FloatField,ObjectIdField
from bson import ObjectId
import datetime
class chatBots(Document):
    user_id=ObjectIdField(required=True)
    name=StringField(required=True, max_length=40)
    text=StringField(null=True)
    validityStartDate=DateTimeField(null=True)
    validityEndDate=DateTimeField(null=True)
    questions=StringField(max_length=24,null=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField(default=datetime.datetime.utcnow)
