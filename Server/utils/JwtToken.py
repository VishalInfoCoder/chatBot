import jwt
import os
from flask import make_response, request,session
import datetime
def generate_token(payload, secret):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)

    # Add the 'exp' claim to the payload
    payload['exp'] = expiration_time

    # Encode the payload and create the JWT token
    token_body = jwt.encode(payload, secret, algorithm="HS256")

    # Construct the complete token 
    token = "Bearer " + token_body

    return token

def validate_token_admin(func):
    secret = os.environ.get('TOKEN_SECRET')
    def wrapper(*args, **kwargs):
        try:
            token = request.headers['Authorization']
            myPayload=token.split(" ")
        except Exception as e:
            return make_response({"message": "Token not provided"}, 403)
        
        try:
            payloads=jwt.decode(myPayload[1], secret, algorithms=["HS256"])
            print(payloads)
            if(payloads['role']=="ADMIN"):
                session['user_id'] = payloads['user_id']
                return func(*args, **kwargs)
            else:
                return make_response({"message": "Invalid User","status":False}) 
        except Exception as e: 
            # print(e)
            return make_response({"message": "Invalid token provided","status":False})   
    wrapper.__name__ = func.__name__
    return wrapper