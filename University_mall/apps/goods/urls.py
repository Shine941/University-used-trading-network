from django.urls import path
from apps.goods.views import GoodsCenterView,GoodsAllView,CategoryGoodsView,MyGoodsView,ConGoodsView
from apps.goods.views import MyBoughtView,MySoldView,MyCollectView,SearchGoodsView,DetailView
urlpatterns = [
    path('newgoods/', GoodsCenterView.as_view()),
    path('Goods/', GoodsAllView.as_view()),
    path('CategoryGoods/<category>/', CategoryGoodsView.as_view()),
    path('MyGoods/', MyGoodsView.as_view()),
    path('controlgoods/<goodsid>/', ConGoodsView.as_view()),
    path('MySolds/', MySoldView.as_view()),
    path('MyBought/', MyBoughtView.as_view()),
    path('MyCollect/', MyCollectView.as_view()),
    path('search/', SearchGoodsView()),
    path('detail/<goodsid>/', DetailView.as_view()),
]
