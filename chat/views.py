from rest_framework import generics, permissions
from utils.enum import USER_ROLE
from api.models import Shop
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class ChatRoomCreateListView(generics.ListCreateAPIView):
      serializer_class = ChatRoomSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = ChatRoom.objects.all()

      def get_queryset(self):
           if self.request.user.role == USER_ROLE.USER:
                self.queryset = self.queryset.filter(client = self.request.user)
                shop_id = self.request.query_params.get('shop_id')
                if shop_id is not None:
                     self.queryset = self.queryset.filter(shop=shop_id)
                     if self.queryset.count() == 0:
                         shop = Shop.objects.filter(id=shop_id).first()
                         chatroom =   ChatRoom.objects.create(
                             client = self.request.user,
                             shop = shop                      
                                 ) 
                         chatroom.save()
                         self.queryset.filter(shop=shop_id,client=self.request.user) 
           elif self.request.user.role == USER_ROLE.SHOP_ADMIN:
                self.queryset = self.queryset.filter(shop=self.request.user.shop)
           return self.queryset
             

class MessageListView(generics.ListAPIView):
      serializer_class = MessageSerializer
      permission_classes = [permissions.IsAuthenticated]
      queryset = Message.objects.all().order_by('-create_date')


      def get_queryset(self):
           
           
           room_id = self.request.query_params.get('room_id')
           if room_id is not None:
                self.queryset = self.queryset.filter(room=room_id)
           return self.queryset
      
