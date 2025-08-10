from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
@shared_task
def my_task(order_id):
     
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)(
          f'order_{order_id}',
          {
               "type":"order.completed",
               "message":f"Order {order_id} is Done!"
          }
     )
