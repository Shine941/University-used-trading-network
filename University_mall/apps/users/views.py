from django.shortcuts import render

# Create your views here.

"""
前端：用户输入用户名后，失去焦点，发送一个axios(ajax)请求
后端：
请求：接受用户名
业务逻辑：根据用户名查询数据库，如果查询结果的数量等于0,说明没有注册，如果查询的数量等于1；数排名有注册
响应：JSON{ code:0,count:0/1,errmsg:ok }
路由：GET     usernames/<username>/count/

"""
from django.views import View
from apps.users.models import User
from django.http import JsonResponse

class UsernameCountView(View):

    def get(self, request, username):
        # 1.接受用户名
        # 2.根据用户名查询数据；
        count= User.objects.filter(username=username).count()
        # 3.返回响应
        return JsonResponse({'code':0,'count':count,'errmsg':'ok'})
