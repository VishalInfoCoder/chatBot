from flask import Blueprint, request
from services.payment_service import initiate_transaction,view_all_plans
payment_route = Blueprint('payment_route', __name__)
from utils.JwtToken import validate_token_admin

@payment_route.route("/api/v1/payment/initiateTransaction", methods=['POST'])
@validate_token_admin
def initiateTransaction():
    data = request.get_json()
    return initiate_transaction(data)
@payment_route.route("/api/v1/payment/viewAllPlans", methods=['POST'])
@validate_token_admin
def viewAllPlans():
    return view_all_plans()
