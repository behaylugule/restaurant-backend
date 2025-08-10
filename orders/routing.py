from django.urls import re_path
from . import consumers


websocket_urlpatterns=[
    re_path(r"ws/orders/(?P<room_id>\d+)/$",consumers.OrdersConsumer.as_asgi())
]