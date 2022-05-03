from django.urls import path
from apps.users.views import UsernameCountView, RegistertView, MobileCountView,StuIdCountView,\
    LoginView,LogoutView,CenterView,ChangeInfoView,ChangeAvatarView

urlpatterns = {
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    # 手机号是否重复
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    # 学号是否重复
    path('stuIds/<stu_id:stu_id>/count/', StuIdCountView.as_view()),
    path('register/', RegistertView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('userinfo/',CenterView.as_view()),
    path('changeinfo/',ChangeInfoView.as_view()),
    path('avaupload/',ChangeAvatarView.as_view()),
}
