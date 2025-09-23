from rest_framework import serializers
from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
     shop_name = serializers.CharField(source = "shop.name")
     client_name = serializers.CharField(source='client.username')

     class Meta:
          model = ChatRoom
          fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
        room_name = serializers.CharField(source='room.shop__name',read_only=True)
        username = serializers.CharField(source='user.username', read_only=True)

        class Meta:
             model = Message
             fields = '__all__' 