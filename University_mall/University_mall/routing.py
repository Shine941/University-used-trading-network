from django.urls import re_path
from apps.chat import consumers

websocket_urlpatterns = [
    # ws接收
    # ws://127.0.0.1:8080/chat/群号/
    # re_path(r'chat/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())
    re_path(r'chat/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi())
]