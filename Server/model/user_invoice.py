from mongoengine import Document, StringField, EmailField,BooleanField,DateTimeField,FloatField
from bson import ObjectId
import datetime
class User_invoices(Document):
    user_id = StringField(required=True, max_length=24)
    transaction_id = StringField(required=True, max_length=24)
    total_amount=FloatField(required=True, max_length=24)
    basic_amount=FloatField(required=True, max_length=24)
    tax_percentage=FloatField(required=True, max_length=24)
    total_tax_values=FloatField(required=True, max_length=24)
    cgst=FloatField(required=True, max_length=24)
    sgst=FloatField(required=True, max_length=24)
    invoice_number=StringField(required=True, max_length=40)
    year=StringField(required=True, max_length=40)
    inv_int=StringField(required=True, max_length=40)
    plan_id=StringField(required=True, max_length=24)
    payment_details=StringField(max_length=50)
    created = DateTimeField(default=datetime.datetime.utcnow)
    updated = DateTimeField(default=datetime.datetime.utcnow)