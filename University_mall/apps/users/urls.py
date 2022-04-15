from django.urls import path
from apps.users.views import UsernameCountView, RegistertView, MobileCountView

urlpatterns = {
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    path('register/', RegistertView.as_view()),
}
