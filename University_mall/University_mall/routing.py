from django.urls import re_path
from apps.chat import consumers

websocket_urlpatterns = [
    # ws接收
    # ws://127.0.0.1:8000/room/群号/
    re_path(r'room/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())
]