from django.urls import path
from apps.chat.views import ChatGoodsView,ChatAlertView,UreadMesView
urlpatterns = {
    path('chatgoods/<goodsid>/', ChatGoodsView.as_view()),
    path('getmessage/', ChatAlertView.as_view()),
    path('ureadmessage/<url>/', UreadMesView.as_view()),
}