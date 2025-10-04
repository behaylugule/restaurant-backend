# chat/routing.py
from django.urls import path, re_path
from .consumers import RestaurantChatConsumer

websocket_urlpatterns = [
   re_path(r"ws/chat-rag/(?P<restaurant_id>\d+)/$", RestaurantChatConsumer.as_asgi()),
]
