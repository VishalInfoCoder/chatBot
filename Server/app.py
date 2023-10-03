import os
from flask import Flask
from flask_cors import CORS
from api.user import user_route 
from api.payment import payment_route
from api.chatbot import chatbot_route
from api.directory import static_bp
from mongoengine import connect 
from dotenv import load_dotenv 
load_dotenv()

os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://ai-ramsol-traning.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "5b60d2473952443cafceeee0b2797cf4"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'
secret = os.environ.get('TOKEN_SECRET')
app = Flask(__name__) 
app.register_blueprint(user_route)
app.register_blueprint(payment_route)
app.register_blueprint(chatbot_route)
app.register_blueprint(static_bp)
# app.register_blueprint(product_route)
app.secret_key = secret
CORS(app)

connect(host=os.environ.get('MONGO_URI'))

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
 