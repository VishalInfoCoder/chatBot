from model.chatbot import chatBots
from model.plan import Plans
from model.userChatHistory import userChatHistory
from flask import jsonify, make_response,session,request
import os
from werkzeug.utils import secure_filename
import datetime
import uuid
import time
import secrets
import string
from datetime import timedelta
from bson import ObjectId
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
from config import client
from langchain.vectorstores import Chroma

from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.llms import AzureOpenAI
import openai 
from langchain.embeddings.openai import OpenAIEmbeddings


os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
os.environ["OPENAI_API_BASE"] = "https://ai-ramsol-traning.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = "5b60d2473952443cafceeee0b2797cf4"
os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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'

   
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                 api_key="5b60d2473952443cafceeee0b2797cf4",
                 api_base="https://ai-ramsol-traning.openai.azure.com/",
                 api_type="azure",
                 api_version="2023-05-15",
                 model_name="embedding-dev")

def get_Answer(data):
    try:
        theBot=session['myBot']
        isUser = userChatHistory.objects[:1](email=data['email'],user_id=theBot['user_id']).first()
        if not isUser:
            isUser=userChatHistory(email=data['email'],history=[],user_id=theBot['user_id'])
            isUser.save()   
        question= data['question']
        #embedding_function = OpenAIEmbeddings()
        #embedding_function = OpenAIEmbeddings()
        print(data['question'])
        embedding_function = OpenAIEmbeddings(
                    api_key="5b60d2473952443cafceeee0b2797cf4",
                    openai_api_base="https://ai-ramsol-traning.openai.azure.com/",
                    openai_api_type="azure",
                    api_version="2023-05-15",
                    deployment="embedding-dev",
                    model="text-embedding-ada-002"
                )
        print(theBot['key'])
        db4 = Chroma(client=client, collection_name=theBot['key'], embedding_function=embedding_function)
        
        
        retriever = db4.as_retriever()
        template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer. 
            Use as much details as possible when responding. 
            Context: {context}
            Question: {question}
            """
    

        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        
        llm = ChatOpenAI(
                deployment_id="Ai-training-example",   
                model_name="gpt-35-turbo", 
                temperature=0.5,
            )
        
        memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)

        qa_chain = ConversationalRetrievalChain.from_llm(
            llm,
                retriever=retriever,
            # chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                verbose=True,
                combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT},
                memory=memory
            )
       
        result = qa_chain({"question": question})
        saveData={}
        saveData['_id'] = ObjectId()
        saveData['question'] = question
        saveData['answer'] = result['answer']
        isUser.history.append(saveData)
        isUser.save()
        updateBot(theBot)
        return make_response({'message':result['answer'] ,"status":True}) 
    except Exception as e:
        print(e)
        return make_response({'message': str(e),"status":False})  
def saveText(key,text):
    #client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection(name=key, embedding_function=openai_ef)
    print(collection.count())

    content =  text

    text_splitter = RecursiveCharacterTextSplitter(
         chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([content])

    for doc in docs:
        uuid_val = uuid.uuid1()
        print("Inserted documents for ", uuid_val)
        collection.add(ids=[str(uuid_val)], documents=doc.page_content)
 
    return jsonify({'status': True})
def add_ChatBot(botdata):
    try:
        free_plan=Plans.objects[:1](description="Free.").first()
        is_bot=chatBots.objects[:1](name=botdata['name'],user_id=session['user_id'])
        is_free_bot=chatBots.objects[:1](plan_name="Free.",user_id=session['user_id'])
        if is_bot:
            return {"message": "chatBot Already Exist","status":False} 
        elif is_free_bot:
            return {"message": "Cant create Chatbot","status":False}
        else:
            current_date = datetime.datetime.utcnow() 
            characters = string.ascii_letters + string.digits
            
            new_date = current_date + timedelta(days=15)
            chatbot=chatBots(user_id=session['user_id'],name=botdata['name'], validityStartDate = current_date,
            validityEndDate = new_date,questions=50,allowed_characters=1000,used_characters=0,plan_name=free_plan['description'],plan_id=free_plan['id'])
            chatbot.save()
            random_key = ''.join(secrets.choice(characters) for _ in range(16))
            final_key = str(chatbot.id) + random_key
            chatbot.update(key=final_key)
            return {"message": "Success","data":str(chatbot.id),"status":True}
    except Exception as e:
        print(e)
        return make_response({'message': str(e),"status":False})      
def get_ChatBot(botdata):
    try:
        myResponse=[]
        isBot = chatBots.objects[:1](id=botdata['id'],user_id=session['user_id']).first()
        if not isBot:
            return {"message": "User does not exists","status":False}
        else: 
            bot_data = {}
            bot_data['_id'] = str(isBot.id)
            bot_data['user_id'] = str(isBot.user_id)
            bot_data['name'] = isBot.name
            # bot_data['text'] = [{'_id': str(item['_id']), 'text_data': item['text_data'], 'title': item['title'], 'user_id': item['user_id']} for item in bot.text]
            bot_data['validityStartDate'] = isBot.validityStartDate
            bot_data['validityEndDate'] = isBot.validityEndDate
            bot_data['questions'] = isBot.questions
            bot_data['used_characters']=isBot.used_characters
            bot_data['allowed_characters']=isBot.allowed_characters
            bot_data['purpose']=isBot.purpose 
            bot_data['company_name']=isBot.company_name
            bot_data['company_description']=isBot.company_description
            bot_data['key']=isBot.key 
            if isBot.avatar_image :
                bot_data['avatar_image']=os.environ.get('url')+isBot.avatar_image 
            bot_data['created'] = isBot.created.isoformat()
            return make_response({"data":bot_data,"status":True}, 200)   
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
            isBot.update(name=editdata['name'],purpose=editdata['purpose'])
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
            current_time=datetime.datetime.utcnow()
            if (isBot.used_characters+len(textData['text'])<isBot.allowed_characters):
                if (isBot.validityEndDate>current_time):
                    saveData={}
                    saveData['_id'] = ObjectId()
                    saveData['text_data'] = textData['text']
                    saveData['title'] = textData['title']
                    saveData['user_id'] = session['user_id']
                    print(saveData) 
                    isBot.text.append(saveData)
                    isBot.used_characters=isBot.used_characters+len(textData['text'])
                    isBot.save()    
                    text_data_concatenated = '\n'.join(item['text_data'] for item in isBot.text)
                    saveText(isBot.key,text_data_concatenated)
                    return {"message": "ChatBot Text Added Successfully","status":True}
                else:
                    return {"message": "Validity Expired","status":False}
            else:
                return {'message': "Limit Exceeded","status":False}
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)   
def add_chatbot_avatar(textData):
    try:
        if 'file' not in textData.files:
            return jsonify({'message': 'No file part',"status":False})
        isBot = chatBots.objects[:1](id=textData.form.get('id'),user_id=session['user_id']).first()
        if not isBot:
            return {"message": "chatBot does not exists","status":False}
        file = textData.files['file']

        if file.filename == '':
            return jsonify({'message': 'No selected file',"status":False})
        current_time = str(datetime.datetime.now().timestamp())
        print(current_time)
        filename = secure_filename(f"{session['user_id']}_{current_time}_{file.filename}")
        print(filename)
        if file:
            filename = os.path.join("assets/images/", filename)
            isBot.avatar_image=filename
            file.save(filename)
            isBot.save()
            return jsonify({'message': 'File uploaded successfully',"status":True})
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)   
def delete_ChatBot_text(textData): 
    try:
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
def get_history(data):
    try:
      theBot=session['myBot']
      print(theBot)
      isUser = userChatHistory.objects[:1](email=data['email'],user_id=theBot['user_id']).first()
      if not isUser:
         return {"message": "NewUser","data":[],"status":True}    
      else:
         botHistory = [{'_id': str(item['_id']), 'question': item['question'], 'answer': item['answer']} for item in isUser.history]
         return make_response({"data": botHistory,"status":True}) 
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404) 
def get_chatBot_Bykey():
    try:
        print("in")
        theBot=session['myBot']
        
        return make_response({"data": theBot,"status":True}) 
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404) 
    
def updateBot(data):
    isBot = chatBots.objects[:1](user_id=data['user_id'],key=data['key']).first()
    if not isBot:
        return {"message": "chatBot does not exists","status":False}
    else:
        isBot.questions=isBot.questions-1
        isBot.save()
def update_company_details(data):
    try:
        isBot = chatBots.objects[:1](user_id=session['user_id'],id=data['id']).first()
        if not isBot:
            return {"message": "chatBot does not exists","status":False}
        else:
            isBot.company_name=data['company_name']
            isBot.company_description=data['company_description']
            isBot.save()
            return {"message": "Company Data Saved","status":True} 
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404)     
def get_chatBot_plan(data):
    try:
        isBot = chatBots.objects[:1](user_id=session['user_id'],id=data['id']).first()
        if not isBot:
            return {"message": "chatBot does not exists","status":False}
        else:
            plan=Plans.objects[:1](id=isBot['plan_id']).first()
            if plan:
                plan_data={'_id': str(plan.id), 'price': plan.price, 'validity': plan.validity, 'description': plan.description, 'title': plan.title, 'questions': plan.questions, 'token_limit': plan.token_limit, 'created': plan.created}
                return make_response({"data": plan_data,"status":True})
            else:
                return {"message": "No plan found! Please upgrade.","status":False}
    except Exception as e:
            print(e)
            return make_response({'message': str(e)}, 404) 
            