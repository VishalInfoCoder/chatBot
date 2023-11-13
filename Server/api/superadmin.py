from flask import Blueprint, request
su_route = Blueprint('su_route', __name__)
from utils.JwtToken import validate_token_superadmin 

from services.user_service import superadmin_login

from services.superadmin_services import view_all_transactions,get_all_users,view_transaction


@su_route.route("/api/v1/su/superadminLogin", methods=['POST'])
def superadminLogin():
    data = request.get_json()
    return superadmin_login(data)


@su_route.route("/api/v1/su/viewAllTransactions", methods=['POST'])
@validate_token_superadmin
def viewAllTransactions():
    data = request.get_json()
    return view_all_transactions(data)

@su_route.route("/api/v1/su/getAllUsers", methods=['POST'])
@validate_token_superadmin
def getAllUsers():
    data = request.get_json()
    return get_all_users(data)
@su_route.route("/api/v1/su/viewTransaction", methods=['POST'])
@validate_token_superadmin
def viewTransaction():
    data = request.get_json()
    return view_transaction(data)