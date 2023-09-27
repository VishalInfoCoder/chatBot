from model.user_transaction import User_transactions
from model.plan import Plans
from model.user_invoice import User_invoices
from flask import jsonify, make_response,session
import os
import datetime
import razorpay
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
            userTransaction = User_transactions(user_id=user_id,plan_id=plan_id,status=status,total_amount=total_amount,currency=currency)
            userTransaction.save()
            transaction_details['id']=str(userTransaction.id)   
            transaction_details['total_amount']=userTransaction.total_amount
            transaction_details['currency']=userTransaction.currency
            order=razorPayInitiate(transaction_details)
            userTransaction.update(order_id=order['id'])
            return {"order_id":order,status:True}
        else:
            return {"message": "Plan Not Found","status":False}    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)     
def getPaymentSuccess(success_data):
    # Initialize the Razorpay client with your API key and secret key
    client = razorpay.Client(auth=(os.environ.get('razor_key'), os.environ.get('razor_secret')))

    # Replace 'YOUR_PAYMENT_ID' with the actual payment ID you want to retrieve details for
    payment_id = success_data['razor_payment_id']
    try:
        # Fetch payment details using the payment ID
        payment = client.payment.fetch(payment_id)

        # Access payment details
        print("Payment Details:")
        print(payment)
    except razorpay.errors.RazorpayError as e:
        print(f"RazorpayError: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")    

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