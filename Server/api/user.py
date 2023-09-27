from flask import Blueprint, request
from services.user_service import signup_service,login_service,edit_user,get_user,get_all_user
user_route = Blueprint('user_route', __name__)
from utils.JwtToken import validate_token_admin

@user_route.route("/api/v1/user/signup", methods=['POST'])
def signup():
    data = request.get_json()
    return signup_service(data)

@user_route.route("/api/v1/user/login", methods=['POST'])
def login():
    data = request.get_json()
    return login_service(data)


@user_route.route("/api/v1/user/editUser", methods=['POST'])
@validate_token_admin
def editUser():
    data = request.get_json()
    return edit_user(data)

@user_route.route("/api/v1/user/getUser", methods=['POST'])
@validate_token_admin
def getUser():
    data = request.get_json() 
    return get_user(data)

@user_route.route("/api/v1/user/getAllUser", methods=['POST'])
@validate_token_admin
def getAllUser():
    data = request.get_json() 
    return get_all_user(data)