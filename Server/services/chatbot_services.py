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
def get_ChatBot(botdata):
    try:
        myResponse=[]
        isBot = chatBots.objects[:1](id=botdata['id'],user_id=session['user_id'])
        if not isBot:
            return {"message": "User does not exists","status":False}
        else: 
            for bot in isBot:
                bot_data = {}
                bot_data['_id'] = str(bot.id)
                bot_data['user_id'] = str(bot.user_id)
                bot_data['name'] = bot.name
                bot_data['text'] = bot.text
                bot_data['validityStartDate'] = bot.validityStartDate
                bot_data['validityEndDate'] = bot.validityEndDate
                bot_data['questions'] = bot.questions
                bot_data['created'] = bot.created.isoformat()
                myResponse.append(bot_data)
                if(len(myResponse)==1):
                    return make_response({"data":myResponse[0],"status":True}, 200)
                else:
                    return make_response({"data":myResponse,"status":True}, 200)    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)
def get_all_ChatBot():
    try:
        myResponse=[]
        isBot = chatBots.objects(user_id=session['user_id'])
        if not isBot:
            return {"message": "User does not exists","status":False}
        else: 
            for bot in isBot:
                bot_data = {}
                bot_data['_id'] = str(bot.id)
                bot_data['user_id'] = str(bot.user_id)
                bot_data['name'] = bot.name
                bot_data['text'] = bot.text
                bot_data['validityStartDate'] = bot.validityStartDate
                bot_data['validityEndDate'] = bot.validityEndDate
                bot_data['questions'] = bot.questions
                bot_data['created'] = bot.created.isoformat()
                myResponse.append(bot_data)
                return make_response({"data":myResponse,"status":True}, 200)    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)