from model.user import Users
from utils.passwordEncryption import encrypt_password, compare_passwords
from utils.JwtToken import generate_token
from flask import jsonify, make_response
import os
import datetime

def signup_service(userdata):
    try:
        email_check = Users.objects[:1](email=userdata['email'])
        if email_check:
            return {"message": "Email Already exists","status":False}
        else:
            name = userdata['name']
            email = userdata['email']
            # image = userdata['image']
            mobile = userdata['mobile']
            address = userdata['address']
            role="ADMIN"
            password = encrypt_password(userdata['password'])

            user = Users(name=name, email=email,
                        mobile=mobile, password=password,is_Active=1,role=role,is_email_verified=0,address=address)
            user.save()

            return make_response({'message': 'Succesfully inserted',"status":True}, 200)

    except Exception as e:
        return make_response({'message': str(e)}, 404)


def login_service(user_credentials):
    try:
        email_check = Users.objects[:1](email=user_credentials['email'])
        if not email_check:
            return {"message": "Email does not exists","status":False}
        else:
            for user in email_check:
                if(user['is_Active']==True):
                    payload = {"email": user['email'], "user_id": str(user['id']),"role":user['role']}
                    secret = os.environ.get('TOKEN_SECRET')
                    if compare_passwords(user_credentials['password'], user['password']):
                        token = generate_token(payload, secret)
                        return make_response({'token': token,"status":True}, 200)
                    else:
                        return make_response({'message': 'Invalid password',"status":False}, 403)
                else:
                    return make_response({'message': 'User is Inactive Please Contact Administration!',"status":False}, 500)
    except Exception as e:
        return make_response({'message': str(e)}, 404)            
def edit_user(editdata): 
    try:
        is_user = Users.objects[:1](id=editdata['id'])
        if not is_user:
            return {"message": "User does not exists","status":False}
        else:
            name = editdata['name']
            email = editdata['email']
            mobile = editdata['mobile']
            is_user.update(name=name,email=email,mobile=mobile,updated=datetime.datetime.utcnow)
            return make_response({'message': 'Succesfully Edited',"status":True}, 200)
    except Exception as e:
        return make_response({'message': str(e)}, 404)
def get_user(viewdata): 
    try:
        myResponse=[]
        
        is_user = Users.objects[:1](id=viewdata['id'])
        if not is_user:
            return {"message": "User does not exists","status":False}
        else: 
            for user in is_user:
                user_data = {}
                user_data['_id'] = str(user.id)
                user_data['name'] = user.name
                user_data['email'] = user.email
                user_data['mobile'] = user.mobile
                myResponse.append(user_data)
                if(len(myResponse)==1):
                    return make_response({"data":myResponse[0],"status":True}, 200)
                else:
                    return make_response({"data":myResponse,"status":True}, 200)    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)
def get_all_user(viewdata): 
    try:
        myResponse=[]
        
        is_user = Users.objects(role="ADMIN")
        if not is_user:
            return {"status": False, "message": "No Users Found"}
        else: 
            for user in is_user:
                user_data = {}
                user_data['_id'] = str(user.id)
                user_data['name'] = user.name
                user_data['email'] = user.email
                user_data['mobile'] = user.mobile
                myResponse.append(user_data)          
        return make_response({"data":myResponse,"status":True}, 200)         
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)
def update_userStatus(viewdata): 
    try:
        is_user = Users.objects[:1](id=viewdata['id'])
        if not is_user:
            return {"status": False, "message": "User does not exists"}
        else: 
            if(is_user.is_Active==0):
                is_user.update(is_Active=1)
                return make_response({"message":"User Changed to Active","status":True}, 200)   
            else:
                is_user.update(is_Active=0)    
                return make_response({"message":"User Changed to Inactive","status":True}, 200)         
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)    