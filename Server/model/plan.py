from mongoengine import Document, StringField, EmailField,BooleanField,DateTimeField,FloatField
from bson import ObjectId
import datetime
class Plans(Document):
    price=FloatField(required=True, max_length=24)
    validity=StringField(required=True, max_length=40)
    description=StringField(required=True, max_length=40)
    title=StringField(required=True, max_length=24)
    questions=StringField(required=True, max_length=24)
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField(default=datetime.datetime.utcnow)