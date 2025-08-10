from datetime import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
       
      
        if self.scope['user'].is_anonymous:
            await self.close()

        else:
            user = self.scope['user']
            self.room_group_name = f'chat_{self.room_id}'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            

            await self.accept()

    
    async def disconnect(self, code):
        return await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data=None, bytes_data=None):
      

        data = json.loads(text_data)
      
        user = self.scope['user']
        message = data['text']
        sender = data['sender']
        databasedata = await self.save_message(self.room_id, user, message,sender)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'text': message,
                'sender':sender,
                'user':user.username,
                'sender_id':user.id,
                'id':databasedata.id,
              
            }
        )

    async def chat_message(self, event):
        if event.get('sender_channel_name')==self.channel_name:
            return
        await self.send(text_data=json.dumps({
            'text':event['text'],
            'username':event['user'],
            'sender':event['sender'],
            'id':event['id']
            
        }))

    @database_sync_to_async
    def save_message(self, room_id, user, message,sender):
        room = ChatRoom.objects.filter(id=room_id).first()
        
        return Message.objects.create(
            room=room,
            sender=sender,
            text=message,
            user = user
        )