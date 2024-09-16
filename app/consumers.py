from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from . import models
from django.contrib.auth.models import User
import datetime


class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept()
        try:
            user_channel = models.User_channel.objects.get(user=self.scope.get("user"))
            user_channel.channel_name = self.channel_name
            user_channel.save() 
        
        except:
            user_channel = models.User_channel()
            user_channel.user = self.scope.get("user") 
            user_channel.channel_name = self.channel_name
            user_channel.save() 
        # print(self.scope.get("url_route").get("kwargs").get('id'))
        self.person_id=self.scope.get("url_route").get("kwargs").get('id')
        
    def receive(self,text_data):
        text_data = json.loads(text_data)
        other_user = User.objects.get(id=self.person_id)
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()
        new_message = models.Message()
        new_message.from_who = self.scope.get("user")
        new_message.to_who = other_user
        new_message.message = text_data.get("message")
        new_message.date=date
        new_message.time = time
        new_message.has_been_seen = False
        new_message.save()
        
        
        try:
            user_channel_name = models.User_channel.objects.get(user=other_user)
            
            data = {"type":"receiver_function",
                    "type_of_data":"new_message",
                    "data":text_data.get("message")}
            async_to_sync(self.channel_layer.send)(user_channel_name.channel_name,data)
        except:
            pass
        
    def receiver_function(self, the_data_that_will_come_from_the_layer):
        data =json.dumps(the_data_that_will_come_from_the_layer)
        self.send(data)        