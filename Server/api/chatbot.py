from flask import Blueprint, request,jsonify, make_response,session
from services.chatbot_services import add_ChatBot,get_ChatBot,get_all_ChatBot,edit_ChatBot,add_ChatBot_text,get_ChatBot_text,delete_ChatBot_text,add_chatbot_avatar,get_Answer,get_history,get_chatBot_Bykey,update_company_details,get_chatBot_plan,get_chat_users,add_chatbot_support,set_chat_bot_theme,setup_facebook_data,get_facebook_data,delete_website_links,train_bot_text,get_my_webLinks,get_trained_webiste_links,toggle_support
from services.chatbot_services import setup_whatsapp_data,get_whatsapp_data,toggel_facebook,toggel_whatsapp,add_chatbot_FAQ,train_bot_faq,get_chatbot_faqs,delete_bot_faq,add_chatbot_doc,train_bot_doc,get_chatbot_doc,delete_bot_doc,add_chatbot_FAQ_byxl,train_bot_FAQ_byxl
chatbot_route = Blueprint('chatbot_route', __name__)
from utils.JwtToken import validate_token_admin,validate_apiKey
import threading



#chat api's
@chatbot_route.route('/api/v1/chatbot/getAnswer', methods=['GET', 'POST'])
@validate_apiKey
def getAnswer():
    data = request.get_json()
    return get_Answer(data)

@chatbot_route.route('/api/v1/chatbot/getChatBotBykey', methods=['GET', 'POST'])
@validate_apiKey
def getChatBotBykey():
    return get_chatBot_Bykey()

#web_api's
@chatbot_route.route("/api/v1/chatbot/addChatBot", methods=['POST'])
@validate_token_admin
def addChatBot():
    data = request.get_json()
    return add_ChatBot(data)

@chatbot_route.route("/api/v1/chatbot/getChatBot", methods=['POST'])
@validate_token_admin
def getChatBot():
    data = request.get_json()
    return get_ChatBot(data)

@chatbot_route.route("/api/v1/chatbot/getAllChatBot", methods=['POST'])
@validate_token_admin
def getAllChatBot():
    data = request.get_json()
    return get_all_ChatBot()
@chatbot_route.route("/api/v1/chatbot/editChatBot", methods=['POST'])
@validate_token_admin
def editChatBot():
    data = request.get_json()
    return edit_ChatBot(data)

@chatbot_route.route("/api/v1/chatbot/addChatBotText", methods=['POST'])
@validate_token_admin
def addChatBotText():
    try:
        data = request.get_json()
        response=add_ChatBot_text(data)    
        if(response['status']==True):
            bg_thread = threading.Thread(target=train_bot_text, args=(data,response['update_id']))
            bg_thread.daemon = True  # Allow the thread to exit when the main process exits
            bg_thread.start()
        return response
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
@chatbot_route.route("/api/v1/chatbot/addChatbotFAQ", methods=['POST'])
@validate_token_admin
def addChatbotFAQ():
    try:
        data = request.get_json()
        response=add_chatbot_FAQ(data)    
        if(response['status']==True):
            bg_thread = threading.Thread(target=train_bot_faq, args=(data,response['update_id'],response['text']))
            bg_thread.daemon = True  # Allow the thread to exit when the main process exits
            bg_thread.start()
        return response
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 

@chatbot_route.route("/api/v1/chatbot/getChatBotText", methods=['POST'])
@validate_token_admin
def getChatBotText():
    data = request.get_json()
    return get_ChatBot_text(data)

@chatbot_route.route("/api/v1/chatbot/getChatbotFaqs", methods=['POST'])
@validate_token_admin
def getChatbotFaqs():
    data = request.get_json()
    return get_chatbot_faqs(data)

@chatbot_route.route("/api/v1/chatbot/getChatbotDoc", methods=['POST'])
@validate_token_admin
def getChatbotDoc():
    data = request.get_json()
    return get_chatbot_doc(data)

@chatbot_route.route("/api/v1/chatbot/deleteChatBotText", methods=['POST'])
@validate_token_admin
def deleteChatBotText():
    try:
        data = request.get_json()
        response=delete_ChatBot_text(data)
        # bg_thread = threading.Thread(target=retrain_bot, args=(data,))
        # bg_thread.daemon = True  # Allow the thread to exit when the main process exits
        # bg_thread.start()
        return response
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
@chatbot_route.route("/api/v1/chatbot/deleteBotFaq", methods=['POST'])
@validate_token_admin
def deleteBotFaq():
    try:
        data = request.get_json()
        response=delete_bot_faq(data)
        # bg_thread = threading.Thread(target=retrain_bot, args=(data,))
        # bg_thread.daemon = True  # Allow the thread to exit when the main process exits
        # bg_thread.start()
        return response
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
@chatbot_route.route("/api/v1/chatbot/deleteBotDoc", methods=['POST'])
@validate_token_admin
def deleteBotDoc():
    try:
        data = request.get_json()
        response=delete_bot_doc(data)
        # bg_thread = threading.Thread(target=retrain_bot, args=(data,))
        # bg_thread.daemon = True  # Allow the thread to exit when the main process exits
        # bg_thread.start()
        return response
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 

@chatbot_route.route("/api/v1/chatbot/addChatbotAvatar", methods=['POST'])
@validate_token_admin
def addChatbotAvatar():
    try:
        print(request)
        return add_chatbot_avatar(request)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
@chatbot_route.route("/api/v1/chatbot/addChatbotFAQByxl", methods=['POST'])
@validate_token_admin
def addChatbotFAQByxl():
    try:
        data = request.get_json()
        res=add_chatbot_FAQ_byxl(data)
        if(res['status']==True):
            bg_thread = threading.Thread(target=train_bot_FAQ_byxl, args=(res['training_data'],res['bot_id']))
            bg_thread.daemon = True  # Allow the thread to exit when the main process exits
            bg_thread.start()
            return res
        else:
            return res
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
@chatbot_route.route("/api/v1/chatbot/addChatbotDoc", methods=['POST'])
@validate_token_admin
def addChatbotDoc():
    try:
        print(request)
        res=add_chatbot_doc(request)
        if(res['status']==True):
            bg_thread = threading.Thread(target=train_bot_doc, args=(res['bot_id'],res['update_id'],res['text']))
            bg_thread.daemon = True  # Allow the thread to exit when the main process exits
            bg_thread.start()
            return res
        else: 
            return res
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404) 
@chatbot_route.route("/api/v1/chatbot/updateCompanyDetails", methods=['POST'])
@validate_token_admin
def updateCompanyDetails():
    try:
        data = request.get_json()
        return update_company_details(data)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)    
@chatbot_route.route("/api/v1/chatbot/getChatBotPlan", methods=['POST'])
@validate_token_admin
def getChatBotPlan():
    try:
        data = request.get_json()
        return get_chatBot_plan(data)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)  

@chatbot_route.route('/api/v1/chatbot/getHistory', methods=['GET', 'POST'])
@validate_token_admin
def getHistory():
    data = request.get_json()
    return get_history(data)    

@chatbot_route.route('/api/v1/chatbot/getChatUsers', methods=['GET', 'POST'])
@validate_token_admin
def getChatUsers():
    try:
        data = request.get_json()
        return get_chat_users(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)#add_chatbot_support
@chatbot_route.route('/api/v1/chatbot/addChatbotSupport', methods=['GET', 'POST'])
@validate_token_admin
def addChatbotSupport():
    try:
        data = request.get_json()
        return add_chatbot_support(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)#
@chatbot_route.route('/api/v1/chatbot/setChatBotTheme', methods=['GET', 'POST'])
@validate_token_admin
def setChatBotTheme():
    try:
        data = request.get_json()
        return set_chat_bot_theme(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)   
@chatbot_route.route('/api/v1/chatbot/setupFacebookData', methods=['GET', 'POST'])
@validate_token_admin
def setupFacebookData():
    try:
        data = request.get_json()
        return setup_facebook_data(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)#
@chatbot_route.route('/api/v1/chatbot/getFacebookData', methods=['GET', 'POST'])
@validate_token_admin
def getFacebookData():
    try:
        data = request.get_json()
        return get_facebook_data(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
@chatbot_route.route('/api/v1/chatbot/setupWhatsappData', methods=['GET', 'POST'])
@validate_token_admin
def setupWhatsappData():
    try:
        data = request.get_json()
        return setup_whatsapp_data(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
@chatbot_route.route('/api/v1/chatbot/getWhatsappData', methods=['GET', 'POST'])
@validate_token_admin
def getWhatsappData():
    try:
        data = request.get_json()
        return get_whatsapp_data(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
@chatbot_route.route('/api/v1/chatbot/getMyWebLinks', methods=['GET', 'POST'])
@validate_token_admin
def getMyWebLinks():
    try:
        data = request.get_json()
        bg_thread = threading.Thread(target=get_my_webLinks, args=(data,))
        bg_thread.daemon = True  # Allow the thread to exit when the main process exits
        bg_thread.start()  
        return {"message":"Fetching all your urls for training this may take a while please wait!","status":True}
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)   
@chatbot_route.route('/api/v1/chatbot/deleteWebsiteLinks', methods=['GET', 'POST'])
@validate_token_admin
def deleteWebsiteLinks():
    try:
        data = request.get_json()
        response=delete_website_links(data)   
        return response
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
@chatbot_route.route('/api/v1/chatbot/getTrainedWebisteLinks', methods=['GET', 'POST'])
@validate_token_admin
def getTrainedWebisteLinks():
    try:
        data = request.get_json()
        return get_trained_webiste_links(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)

@chatbot_route.route('/api/v1/chatbot/toggleSupport', methods=['GET', 'POST'])
@validate_token_admin
def toggleSupport():
    try:
        data = request.get_json()
        return toggle_support(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
    
@chatbot_route.route('/api/v1/chatbot/toggelWhatsapp', methods=['GET', 'POST'])
@validate_token_admin
def toggelWhatsapp():
    try:
        data = request.get_json()
        return toggel_whatsapp(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
    
@chatbot_route.route('/api/v1/chatbot/toggelFacebook', methods=['GET', 'POST'])
@validate_token_admin
def toggelFacebook():
    try:
        data = request.get_json()
        return toggel_facebook(data)    
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)
    
