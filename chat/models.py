from django.db import models
from utils.commons_model import CommonsModel
from api.models import CustomUser, Shop
from utils.enum import MESSAGE_SENDER


class ChatRoom(CommonsModel):
      client = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.CASCADE, related_name='client_chat')
      shop = models.ForeignKey(Shop, null=False, blank=False, on_delete=models.CASCADE, related_name='shop_chat')

      def __str__(self):
           return self.client.username + " - " + self.shop.name


class Message (CommonsModel):
      room = models.ForeignKey(ChatRoom, null=False, blank=False, on_delete=models.CASCADE, related_name='room_message')
      user = models.ForeignKey(CustomUser, null=False, blank=False,  on_delete=models.CASCADE, related_name='sender_message')
      text= models.TextField(blank=True, null=True)
      sender = models.CharField(max_length=20, choices=MESSAGE_SENDER.choices, default=MESSAGE_SENDER.USER)

      def __str__(self):
           return self.sender
