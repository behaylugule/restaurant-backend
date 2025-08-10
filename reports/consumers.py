import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

User = get_user_model()


class ReportsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]['kwargs']['room_id']

        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            user = self.scope['user']
            self.room_group_name = f'reports_for_{self.room_id}'
            print("WebSocket connected:", self.channel_name)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
    
    async def disconnect(self, code):
        return await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data=None, bytes_data=None):
          data = json.loads(text_data)
          await self.channel_layer.group_send(
              self.room_group_name,
              {
                  'type': 'send_report',
                  'report': data
              }
          )
    
    async def send_report(self, event):
        report = event['report']
        await self.send(text_data=json.dumps(report))

