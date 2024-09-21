from channels.consumer import SyncConsumer
import json
from asgiref.sync import async_to_sync 
from .models import Chat, Group

class NewConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('----------------------------------')
        print(self.scope)

        # print("xxxxxxx", self.scope['user'])
        self.group_name=self.scope['url_route']['kwargs']['groupname']
        self.group_check=Group.objects.filter(name=self.group_name).first()
        
        if not self.group_check:
            group=Group.objects.create(name=self.group_name)
            
    
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type': 'websocket.accept',
        })
        

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def websocket_receive(self, event):
        print(self.scope)
        user=self.scope.get('user')
        if user:
            async_to_sync(self.channel_layer.group_send)(self.group_name, {
                'type': 'chat.message',
                'message': event['text']
            })
            chat = json.loads(event['text'])
            group=Group.objects.get(name=self.group_name)
            chat_instance=Chat.objects.create(group=group, conversation=chat['msg'])
        else:
            self.send({
            'type': 'websocket.send',
            'text': 'login required'
        })
        

    def chat_message(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
        