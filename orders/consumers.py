import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import ValidationError

from api.models import DinningTable, Menu, Shop
from orders.models import Order, OrderItem
from orders.serializers import KitchenDisplaySerializer
from utils.enum import ORDER_STATUS, USER_ROLE

User = get_user_model()

class OrdersConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        if self.scope['user'].is_anonymous:
            await self.close()
        
        else:
            user= self.scope['user']
            if user.role == USER_ROLE.SHOP_ADMIN:
                self.room_group_name = f'kitchen_dispaly_{self.room_id}'
            else:
                self.room_group_name = f'customer_order{self.room_id}_{user.id}'
            
            await self.channel_layer.group_add(self.room_group_name,self.channel_name)

            await self.accept()
    
    async def disconnect(self, code):
          return await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    

    async def receive(self, text_data=None, bytes_data=None):
            data = json.loads(text_data)
            user=self.scope['user']
            if user.role == USER_ROLE.SHOP_ADMIN:  
                 updateOrder = await self.update_order(data['method'],data['order_id'])
                 await self.channel_layer.group_send(
                      f'customer_order{self.room_id}_{updateOrder.get("user")}',
                      {
                           'type':'send_order',
                           'order':updateOrder
                      }
                 )

                 await self.channel_layer.group_send(
                      f'kitchen_dispaly_{user.id}',
                      {
                           'type':'send_order',
                           'order':updateOrder
                      }
                  )
            elif user.role == USER_ROLE.USER:
                
                 orderCreated = await self.create_order(data)
                 await self.channel_layer.group_send(
                      f'kitchen_dispaly_{orderCreated.get("shop")}',
                      {
                           'type':'send_order',
                           'order':orderCreated
                      }
                 )

                 await self.channel_layer.group_send(
                       f'customer_order{self.room_id}_{user.id}',
                      {
                           'type':'send_order',
                           'order':orderCreated
                      }
                 )

    async def send_order(self,event):
         await self.send(text_data=json.dumps(event['order']))
    


    @database_sync_to_async
    def create_order(self,data=None,request=None):
           shop = Shop.objects.filter(id=data['shop']).first()
           diningTable = DinningTable.objects.filter(id=data['table_number']).first()
           order = Order.objects.create(
                shop=shop,
                user= self.scope['user'],
                total_price = data['total_price'],
                table_number = diningTable
           )
           order.save()
           for item in data['items']:
                menu = Menu.objects.filter(id=item['id']).first()
                orderItem =  OrderItem.objects.create(
                    shop= shop , 
                    order = order, 
                    menu = menu,
                    price = item['price'],
                    quantity=item['quantity']
                 )
                orderItem.save() 

           serializer = KitchenDisplaySerializer(order, context={'request': request} if request else {})
           
           return serializer.data

    @database_sync_to_async
    def update_order(self, method,order_id,request=None):
           instance = Order.objects.get(id=order_id)
         
           if method == 'cancled':
                if instance.status != ORDER_STATUS.PENDING:
                     raise ValidationError("The order status is not pending")
                instance.status = ORDER_STATUS.CANCLED
                instance.save()
                 
           if method == ORDER_STATUS.PROCESSING:
                if instance.status !=ORDER_STATUS.PENDING:
                     raise ValidationError('The order status is not pending')
                instance.status = ORDER_STATUS.PROCESSING
                instance.save()
           if method == ORDER_STATUS.READY:
                if instance.status != ORDER_STATUS.PROCESSING:
                    raise ValidationError('The order status is not Processing')
                instance.status = ORDER_STATUS.READY
                instance.save()
           if method == 'completed':
                if instance.status != ORDER_STATUS.READY:
                     raise ValidationError("The order status is not pending")
                instance.status = ORDER_STATUS.COMPLETED
                instance.save()  
           serializer = KitchenDisplaySerializer(instance, context={'request': request} if request else {})
          
           return serializer.data 
          