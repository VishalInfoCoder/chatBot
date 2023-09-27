from flask import Blueprint, request
from services.payment_service import initiate_transaction
payment_route = Blueprint('payment_route', __name__)
from utils.JwtToken import validate_token_admin

@payment_route.route("/api/v1/payment/initiateTransaction", methods=['POST'])
@validate_token_admin
def initiateTransaction():
    data = request.get_json()
    return initiate_transaction(data)
