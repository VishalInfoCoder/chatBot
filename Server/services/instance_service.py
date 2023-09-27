from model.instance import Instances
from flask import jsonify, make_response,session
import os
import datetime

def add_instance(instance_data):
    try:
        print(session['user_id'])
        instance_exist = Instances.objects[:1](user_id=session['user_id'])
        if instance_exist:
            return {"message": "Instance Already exists","status":False}
        else:
            instance_key = instance_data['instance_key']
            instance_secret = instance_data['instance_secret']
            # image = userdata['image']
            current_datetime = datetime.datetime.now()
            # Add 15 days to the current datetime
            new_datetime = current_datetime + datetime.timedelta(days=15)
            print("Current Datetime:", current_datetime)
            print("Datetime after adding 15 days:", new_datetime)
            validity_start_date = current_datetime
            validity_end_date=new_datetime
            user_id = session['user_id']
            instance = Instances(instance_key=instance_key,instance_secret=instance_secret,validity_start_date=validity_start_date,validity_end_date=validity_end_date,user_id=user_id)
            instance.save()
            return make_response({'message': 'Instance Created Successfully',"status":True}, 200)
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)
    
def view_user_instance(instance_data):
    try:
        myResponse=[]
        instance_exist = Instances.objects[:1](user_id=session['user_id'])
        if not  instance_exist:
            return {"message": "Instance Not Found","status":False}
        else:
             for instance in instance_exist:
                instance_data = {}
                instance_data['_id'] = str(instance.id)
                instance_data['user_id'] = instance.user_id
                instance_data['instance_key'] = instance.instance_key
                instance_data['instance_secret'] = instance.instance_secret
                instance_data['validity_start_date'] = instance.validity_start_date
                instance_data['validity_end_date'] = instance.validity_end_date
                myResponse.append(instance_data)
                if(len(myResponse)==1):
                    return make_response({"user":myResponse[0],"status":True}, 200)
                else:
                    return make_response({"user":myResponse,"status":True}, 200)    
    except Exception as e:
        print(e)
        return make_response({'message': str(e)}, 404)