from flask import Blueprint, request
from services.chatbot_services import add_ChatBot,get_ChatBot
chatbot_route = Blueprint('chatbot_route', __name__)
from utils.JwtToken import validate_token_admin


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