from mongoengine import Document, StringField, EmailField,BooleanField,DateTimeField,FloatField,ObjectIdField,IntField,ListField,DictField
from bson import ObjectId
import datetime
class chatBots(Document):
    user_id=ObjectIdField(required=True)
    allowed_characters=IntField(max_length=10,null=True,default=0)
    used_characters=IntField(max_length=10,null=True,default=0)
    name=StringField(required=True, max_length=40)
    text = ListField(DictField(
        _id=ObjectIdField(),
        text_data=StringField(),
        user_id=ObjectIdField(),
        title=StringField()
    ))
    validityStartDate=DateTimeField(null=True)
    validityEndDate=DateTimeField(null=True)
    purpose=StringField(max_length=40,null=True)
    questions=IntField(max_length=10,null=True)
    key=StringField(max_length=40)
    avatar_image=StringField()
    company_name=StringField(max_length=40)
    company_description=StringField(max_length=40)
    plan_id=ObjectIdField()
    support_name=StringField(max_length=40)
    support_email=StringField(max_length=40)
    support_mobile=StringField(max_length=40)
    plan_name=StringField(max_length=40)
    theme=StringField(max_length=40)
    facebookData=DictField(
        fbAppId=StringField(),
        fbAppSecret=StringField(),
        fbPageName=StringField(),
        fbPageId=StringField(),
        fbPageAccessToken=StringField(),
    )
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField(default=datetime.datetime.utcnow) 
