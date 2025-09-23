from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('rooms/', views.ChatRoomCreateListView.as_view(), name='chat_room_list'),
]