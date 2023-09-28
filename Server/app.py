import os
from flask import Flask
from flask_cors import CORS
from api.user import user_route 
from api.payment import payment_route
from api.chatbot import chatbot_route
from mongoengine import connect 
from dotenv import load_dotenv 
load_dotenv()
secret = os.environ.get('TOKEN_SECRET')

app = Flask(__name__) 
app.register_blueprint(user_route)
app.register_blueprint(payment_route)
app.register_blueprint(chatbot_route)
# app.register_blueprint(product_route)
app.secret_key = secret
CORS(app)

connect(host=os.environ.get('MONGO_URI'))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
 