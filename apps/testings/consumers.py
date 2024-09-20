from channels.consumer import SyncConsumer
import json
from asgiref.sync import async_to_sync 

class NewConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.group_name=self.scope['url_route']['kwargs']['groupname']
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })
        

    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def websocket_receive(self, event):
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            'type': 'chat.message',
            'message': event['text']
        })
       
        # self.send({

    def chat_message(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
        