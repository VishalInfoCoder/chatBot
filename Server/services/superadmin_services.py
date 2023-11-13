from model.user import Users
from flask import jsonify, make_response,Flask, render_template, request,session
from model.user_invoice import User_invoices
from model.user_transaction import User_transactions
from model.plan import Plans
import datetime


def get_all_users(viewdata): 
    try:
        myResponse=[]
        if viewdata['page']:
            page=viewdata['page']
        else:
            page=0  
        per_page=10      
        skip = (page - 1) * per_page
        is_user = Users.objects(role="ADMIN").skip(skip).limit(per_page)
        total_count = Users.objects(role="ADMIN").count()
        if not is_user:
            return {"status": False, "message": "No Users Found"}
        else: 
            
            for user in is_user:
                user_data = {}
                user_data['_id'] = str(user.id)
                user_data['name'] = user.name
                user_data['email'] = user.email
                user_data['mobile'] = user.mobile
                user_data['referal_code']=user.referal_code
                myResponse.append(user_data)          
        return make_response({"data":myResponse,"count":total_count,"status":True}, 200)         
    except Exception as e:
       
        return make_response({'message': str(e)}, 404)
def view_all_transactions(userdata):
    try:
        myResponse=[]
        if userdata['page']:
            page=userdata['page']
        else:
            page=0  
        per_page=10      
        skip = (page - 1) * per_page
        today_date = datetime.datetime.now()
        if 'fromDate' in userdata:
            from_date = datetime.datetime.strptime(userdata['fromDate'], '%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            from_date = today_date.replace(hour=0, minute=0, second=0, microsecond=0)
        if 'toDate' in userdata:
            to_date = datetime.datetime.strptime(userdata['toDate'], '%Y-%m-%d').replace(hour=23, minute=59, second=59, microsecond=999)  
        else: 
            to_date = today_date.replace(hour=23, minute=59, second=59, microsecond=999)
        query = {
        'created__gte': from_date,
        'created__lte': to_date
         }
        data=User_invoices.objects(**query).skip(skip).limit(per_page)
        total_count = User_invoices.objects(**query).count()
        myResponse.extend([{'_id':str(transaction_data.id),'user_id': str(transaction_data.user_id), 'total_amount': transaction_data.total_amount, 'basic_amount': transaction_data.basic_amount, 'tax_percentage': transaction_data.tax_percentage, 'total_tax_values': transaction_data.total_tax_values, 'cgst': transaction_data.cgst,'sgst': transaction_data.sgst, 'invoice_number': transaction_data.invoice_number,'payment_details': transaction_data.payment_details,'refered_by':transaction_data['refered_by'] ,'created': transaction_data.created} for transaction_data in data])
        return make_response({"data":myResponse,"count":total_count,"status":True}, 200)
    except Exception as e:
       
        return make_response({'message': str(e)}, 404) 
def view_transaction(userdata):
    try:
        myResponse={}
        transaction_data=User_invoices.objects(id=userdata['id']).first()
        myResponse={'_id':str(transaction_data.id),'user_id': str(transaction_data.user_id), 'total_amount': transaction_data.total_amount, 'basic_amount': transaction_data.basic_amount, 'tax_percentage': transaction_data.tax_percentage, 'total_tax_values': transaction_data.total_tax_values, 'cgst': transaction_data.cgst,'sgst': transaction_data.sgst, 'invoice_number': transaction_data.invoice_number,'payment_details': transaction_data.payment_details, 'created': transaction_data.created}
        return make_response({"data":myResponse,"status":True}, 200)
    except Exception as e:
       
        return make_response({'message': str(e)}, 404) 