from django.urls import path
from apps.chat.views import ChatCenterView
urlpatterns = {
    path('chat/', ChatCenterView.chat),
}