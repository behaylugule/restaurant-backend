# chat/routing.py
from django.urls import path
from .consumers import ResumeChatConsumer

websocket_urlpatterns = [
    path("ws/chat-rag/", ResumeChatConsumer.as_asgi()),
]
