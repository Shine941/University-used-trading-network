from django.urls import path
from apps.users.views import UsernameCountView, RegistertView, MobileCountView,StuIdCountView,\
    StuNameCountView

urlpatterns = {
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    # 手机号是否重复
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view()),
    # 学号是否重复
    path('stuIds/<stu_id:stu_id>/count/', StuIdCountView.as_view()),
    #  姓名是否重复
    path('stunames/<stu_name:stu_name>/count/', StuNameCountView.as_view()),
    path('register/', RegistertView.as_view()),
}
