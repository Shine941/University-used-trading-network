from django.urls import path
from apps.goods.views import GoodsCenterView,GetGoodsAllView

urlpatterns = {
    # 判断用户名是否重复
    path('newgoods/', GoodsCenterView.as_view()),
    path('Goods/', GetGoodsAllView.as_view()),
}