from flask import Blueprint, request,jsonify, make_response,session
from services.chatbot_services import add_ChatBot,get_ChatBot,get_all_ChatBot,edit_ChatBot,add_ChatBot_text,get_ChatBot_text,delete_ChatBot_text,add_chatbot_avatar,get_Answer,get_history,get_chatBot_Bykey
chatbot_route = Blueprint('chatbot_route', __name__)
from utils.JwtToken import validate_token_admin,validate_apiKey







#chat api's
@chatbot_route.route('/api/v1/chatbot/getAnswer', methods=['GET', 'POST'])
@validate_apiKey
def getAnswer():
    data = request.get_json()
    return get_Answer(data)

@chatbot_route.route('/api/v1/chatbot/getHistory', methods=['GET', 'POST'])
@validate_apiKey
def getHistory():
    data = request.get_json()
    return get_history(data)

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
    data = request.get_json()
    return add_ChatBot_text(data)

@chatbot_route.route("/api/v1/chatbot/getChatBotText", methods=['POST'])
@validate_token_admin
def getChatBotText():
    data = request.get_json()
    return get_ChatBot_text(data)

@chatbot_route.route("/api/v1/chatbot/deleteChatBotText", methods=['POST'])
@validate_token_admin
def deleteChatBotText():
    data = request.get_json()
    return delete_ChatBot_text(data)

@chatbot_route.route("/api/v1/chatbot/addChatbotAvatar", methods=['POST'])
@validate_token_admin
def addChatbotAvatar():
    try:
        print(request)
        return add_chatbot_avatar(request)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)    