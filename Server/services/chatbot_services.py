from model.chatbot import chatBots
from flask import jsonify, make_response,session
import os
import datetime
from datetime import timedelta
from bson import ObjectId
def add_ChatBot(botdata):
    try:
        is_bot=chatBots.objects[:1](name=botdata['name'],user_id=session['user_id'])
        if is_bot:
            return {"message": "chatBot Already Exist","status":False} 
        else:
            current_date = datetime.datetime.utcnow() 
            new_date = current_date + timedelta(days=15)
            chatbot=chatBots(user_id=session['user_id'],name=botdata['name'], validityStartDate = current_date,
            validityEndDate = new_date,questions=50,allowed_characters=1000,used_characters=0)
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
                print(bot.text)
                bot_data = {}
                bot_data['_id'] = str(bot.id)
                bot_data['user_id'] = str(bot.user_id)
                bot_data['name'] = bot.name
                # bot_data['text'] = [{'_id': str(item['_id']), 'text_data': item['text_data'], 'title': item['title'], 'user_id': item['user_id']} for item in bot.text]
                bot_data['validityStartDate'] = bot.validityStartDate
                bot_data['validityEndDate'] = bot.validityEndDate
                bot_data['questions'] = bot.questions
                bot_data['used_characters']=bot.used_characters
                bot_data['allowed_characters']=bot.allowed_characters 
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
                # bot_data['text'] = [{'_id': str(item['_id']), 'text_data': item['text_data'], 'title': item['title'], 'user_id': item['user_id']} for item in bot.text]
                bot_data['validityStartDate'] = bot.validityStartDate
                bot_data['validityEndDate'] = bot.validityEndDate
                bot_data['questions'] = bot.questions
                bot_data['used_characters']=bot.used_characters
                bot_data['allowed_characters']=bot.allowed_characters 
                bot_data['created'] = bot.created.isoformat()
                myResponse.append(bot_data)
            return make_response({"data":myResponse,"status":True}, 200)    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)
def edit_ChatBot(editdata):
    try:
        myResponse=[]
        isBot = chatBots.objects[:1](id=editdata['id'],user_id=session['user_id'])
        if not isBot:
            return {"message": "User does not exists","status":False}
        else: 
            isBot.update(name=editdata['name'])
            return make_response({'message': 'Succesfully Edited',"status":True}, 200) 
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)
def get_ChatBot_text(textData):
    try:
        isBot = chatBots.objects[:1](id=textData['id'],user_id=session['user_id']).first()
        if not isBot:
            return {"message": "chatBot does not exists","status":False}
        else: 
            botData = [{'_id': str(item['_id']), 'text_data': item['text_data'], 'title': item['title'], 'user_id': item['user_id']} for item in isBot.text]
            return make_response({'data':botData ,"status":True}, 200) 
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)    
def add_ChatBot_text(textData):
    try:
        myResponse=[]
        saveData={}
        isBot = chatBots.objects[:1](id=textData['id'],user_id=session['user_id']).first()
        if not isBot:
            return {"message": "chatBot does not exists","status":False}
        else: 
            if isBot.used_characters+len(textData['text'])<isBot.allowed_characters:
                saveData={}
                saveData['_id'] = ObjectId()
                saveData['text_data'] = textData['text']
                saveData['title'] = textData['title']
                saveData['user_id'] = session['user_id']
                print(saveData) 
                isBot.text.append(saveData)
                isBot.used_characters=isBot.used_characters+len(textData['text'])
                isBot.save()    
                return {"message": "ChatBot Text Added Successfully","status":True}
            else:
                return {'message': "Limit Exceeded","status":False}
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)     
def delete_ChatBot_text(textData):
    try:
        saveData={}
        newdata=[]
        isBot = chatBots.objects[:1](id=textData['id'],user_id=session['user_id']).first()
        if not isBot:
            return {"message": "chatBot does not exists","status":False}
        else: 
            bot_text = [{'_id': str(item['_id']), 'text_data': item['text_data'], 'title': item['title'], 'user_id': item['user_id']} for item in isBot.text]
            newdata[:] = [item for item in bot_text if item["_id"] != textData['text_id']]
            isBot.text=newdata
            newCount = sum(len(item['text_data']) for item in newdata)
            isBot.used_characters=newCount
            isBot.save()
            return {"message": "ChatBot Text Removed Successfully","status":True}
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)       