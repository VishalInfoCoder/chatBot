from model.chatbot import chatBots
from flask import jsonify, make_response,session
import os
import datetime

def add_ChatBot(botdata):
    try:
        is_bot=chatBots.objects[:1](name=botdata['name'],user_id=session['user_id'])
        if is_bot:
            return {"message": "chatBot Already Exist","status":False} 
        else:
            chatbot=chatBots(user_id=session['user_id'],name=botdata['name'])
            chatbot.save()
            return {"message": "Success","data":str(chatbot.id),"status":True}
    except Exception as e:
        print(e)
        return make_response({'message': str(e),"status":False})      