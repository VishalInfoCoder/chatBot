from model.user_transaction import User_transactions
from model.plan import Plans
from model.user_invoice import User_invoices
from model.chatbot import chatBots
from flask import jsonify, make_response,session
import os
import datetime
from datetime import timedelta
import razorpay
from mongoengine import Q
def initiate_transaction(transaction_data):
    try:
        plan_data=Plans.objects[:1](id=transaction_data['plan_id'])
        if plan_data:
            transaction_details={}
            user_id=session['user_id']
            price=plan_data[0]['price']
            plan_id=transaction_data['plan_id']
            status="Pending"
            Gstpercentage = 5
            currency="INR"
            GstAmount = (price * Gstpercentage)/100
            total_amount =price +GstAmount
            userTransaction = User_transactions(user_id=user_id,plan_id=plan_id,status=status,total_amount=total_amount,currency=currency,chatbot_id=transaction_data['chatbot_id'])
            userTransaction.save()
            transaction_details['id']=str(userTransaction.id)   
            transaction_details['total_amount']=userTransaction.total_amount*100
            transaction_details['currency']=userTransaction.currency
            order=razorPayInitiate(transaction_details)
            userTransaction.update(order_id=order['id'])
            return {"order_id":order,"status":True}
        else:
            return {"message": "Plan Not Found","status":False}    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)     
def get_PaymentSuccess(success_data):
    # Initialize the Razorpay client with your API key and secret key
    client = razorpay.Client(auth=(os.environ.get('razor_key'), os.environ.get('razor_secret')))

    # Replace 'YOUR_PAYMENT_ID' with the actual payment ID you want to retrieve details for
    payment_id = success_data['razorpay_payment_id']
    try:
        current_year = datetime.datetime.now().year
        # Fetch payment details using the payment ID
        payment = client.payment.fetch(payment_id)
        transaction_data=User_transactions.objects[:1](order_id=success_data['razorpay_order_id']).first()
        plan_data=Plans.objects[:1](id=transaction_data['plan_id']).first()
        invoice_data=User_invoices.objects[:1](user_id=transaction_data['user_id']).order_by('-inv_int').first() 
        if invoice_data:
            intInc=int(invoice_data["inv_int"])+1 
            inv_int=set_invoiceNumber(intInc)
            newInv="INV-"+str(current_year)+str(inv_int)
            create_user_invoice=User_invoices(chatbot_id=transaction_data['chatbot_id'],user_id=transaction_data['user_id'],transaction_id=transaction_data['id'],total_amount=transaction_data['total_amount'],basic_amount=plan_data['price'],tax_percentage='5',total_tax_values=00000000.1,cgst=2.5,sgst=2.5,invoice_number=newInv,year=str(current_year),inv_int=intInc,plan_id=plan_data['id'],payment_details=payment)
            create_user_invoice.save()
            transaction_data.update(status='paid')
            updateChatBot(transaction_data['chatbot_id'],plan_data)
        else:
            intInc=1 
            inv_int=set_invoiceNumber(intInc)
            newInv="INV-"+str(current_year)+str(inv_int)
            create_user_invoice=User_invoices(chatbot_id=transaction_data['chatbot_id'],user_id=transaction_data['user_id'],transaction_id=transaction_data['id'],total_amount=transaction_data['total_amount'],basic_amount=plan_data['price'],tax_percentage='5',total_tax_values=00000000.1,cgst=2.5,sgst=2.5,invoice_number=newInv,year=str(current_year),inv_int=intInc,plan_id=plan_data['id'],payment_details=payment)
            create_user_invoice.save()   
            transaction_data.update(status='paid')
            updateChatBot(transaction_data['chatbot_id'],plan_data)
        # Access payment details
        return {"message":"Upgraded Successfully","status":True}
    except Exception as e:
        print(f"An error occurred: {str(e)}")    
        return {'message': str(e),"status":False}

def razorPayInitiate(transaction_details):
    

    # Initialize Razorpay client with your API Key and Secret Key
    client = razorpay.Client(auth=(os.environ.get('razor_key'), os.environ.get('razor_secret')))
    # Create a payment order
    order_amount = int(transaction_details['total_amount']) # Amount in paise (e.g., 50000 paise = ₹500)
    order_currency = transaction_details['currency']
    order_receipt = transaction_details['id']  # You should generate a unique receipt ID

    order = client.order.create({
        "amount": order_amount,
        "currency": order_currency,
        "receipt": order_receipt
    })

    # Get the order ID from the response
      
    return order

def view_all_plans():
    try:
        myResponse=[]
        my_plans=Plans.objects().order_by("created")
        if not my_plans:
            return {"message": "Plans Not Found","status":False}
        else:
            myResponse.extend([{'_id': str(plan.id), 'price': plan.price, 'validity': plan.validity, 'description': plan.description, 'title': plan.title, 'questions': plan.questions, 'token_limit': plan.token_limit, 'created': plan.created} for plan in my_plans])      
            myResponse.insert(0, myResponse.pop())    
            return make_response({"data":myResponse,"status":True}, 200)        
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)    
def set_invoiceNumber(i):
    i=int(i)
    if(i<9) :
        invInt="0000"+str(i)
    elif (i>=999):
        invInt="0"+str(i)
    elif (i>=99):
        invInt="00"+str(i)
    elif (i>=9):
        invInt="000"+str(i)
    else:
        invInt=i
    return invInt
def updateChatBot(chatbot_id,plan):
    try:
        bot_data=chatBots.objects[:1](id=chatbot_id).first()
        current_date = datetime.datetime.utcnow() 
        new_date = current_date + timedelta(days=30)
        print (bot_data['validityEndDate'])
        if bot_data['validityEndDate'] is None:
            bot_data.questions = int(plan['questions'])
            bot_data.allowed_characters = int(plan['token_limit'])
            bot_data.validityStartDate = current_date
            bot_data.validityEndDate = new_date
            bot_data.plan_id=plan['id']
            bot_data.plan_name=plan['description']
            bot_data.save()
        elif  bot_data['validityEndDate'] < current_date:
            bot_data.questions = bot_data.questions+int(plan['questions'])
            bot_data.allowed_characters = int(plan['token_limit'])
            bot_data.validityStartDate = current_date
            bot_data.validityEndDate = new_date
            bot_data.plan_id=plan['id']
            bot_data.plan_name=plan['description']
            bot_data.save()
        else:
            bot_data.questions = bot_data.questions+int(plan['questions'])
            bot_data.validityEndDate =bot_data.validityEndDate + timedelta(days=30)
            bot_data.allowed_characters = int(plan['token_limit'])
            bot_data.plan_id=plan['id']
            bot_data.plan_name=plan['description']
            bot_data.save()
        return True
    except Exception as e:
        print(e)
        return False
def view_all_transactions(userdata):
    try:
        myResponse=[]
        if userdata['page']:
            page=userdata['page']
        else:
            page=0  
        per_page=10      
        skip = (page - 1) * per_page
        data=User_invoices.objects(user_id=session['user_id'],chatbot_id=userdata['chatbot_id']).skip(skip).limit(per_page)
        total_count = User_invoices.objects(user_id=session['user_id'],chatbot_id=userdata['chatbot_id']).count()
        myResponse.extend([{'_id':str(transaction_data.id),'user_id': str(transaction_data.user_id), 'total_amount': transaction_data.total_amount, 'basic_amount': transaction_data.basic_amount, 'tax_percentage': transaction_data.tax_percentage, 'total_tax_values': transaction_data.total_tax_values, 'cgst': transaction_data.cgst,'sgst': transaction_data.sgst, 'invoice_number': transaction_data.invoice_number,'payment_details': transaction_data.payment_details, 'created': transaction_data.created} for transaction_data in data])
        return make_response({"data":myResponse,"count":total_count,"status":True}, 200)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
def view_transaction(userdata):
    try:
        myResponse={}
        transaction_data=User_invoices.objects(user_id=session['user_id'],id=userdata['id']).first()
        myResponse={'_id':str(transaction_data.id),'user_id': str(transaction_data.user_id), 'total_amount': transaction_data.total_amount, 'basic_amount': transaction_data.basic_amount, 'tax_percentage': transaction_data.tax_percentage, 'total_tax_values': transaction_data.total_tax_values, 'cgst': transaction_data.cgst,'sgst': transaction_data.sgst, 'invoice_number': transaction_data.invoice_number,'payment_details': transaction_data.payment_details, 'created': transaction_data.created}
        return make_response({"data":myResponse,"status":True}, 200)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 