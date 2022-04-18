import re

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
from django.shortcuts import render


# 用户名重名验证
class UsernameCountView(View):

    def get(self, request, username):
        # 1.接受用户名，对这个用户名进行一个判断
        # if not re.match('[a-zA-Z0-9_-]{2,20}',username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名不满足需求'})
        # 2.根据用户名查询数据；
        count = User.objects.filter(username=username).count()
        # 3.返回响应
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class MobileCountView(View):

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class StuNameCountView(View):
    def get(self, request, stu_name):
        count = User.objects.filter(stu_name=stu_name).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class StuIdCountView(View):
    def get(self, request, stu_id):
        count = User.objects.filter(stu_id=stu_id).count()
        print(count)
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


# *********************注册***********************
import json


class RegistertView(View):
    def post(self, request):
        # 1.接受请求
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        # 2.获取数据
        username = body_dict.get('username')
        phone = body_dict.get('phone')
        name = body_dict.get('name')
        stu_id = body_dict.get('stu_id')
        stu_class = body_dict.get('class')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        gender = body_dict.get('gender')
        # 3.验证数据
        #     3.1都要有
        #     all里面的元素只要是None就返回false
        if not all([username, password, phone, name, stu_id, password2, gender]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[a-zA-Z0-9_-]{2,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        #     3.2用户名验证，不能重复
        if User.objects.filter(username=username).count():
            return JsonResponse({'code': 400, 'errmsg': '用户名不能重复'})
        #     3.3密码非空
        #     3.4确认密码和密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '密码与确认密码不一致'})
        #     3.5 手机号满足规则，手机号学号不能重复
        if User.objects.filter(stu_id=stu_id).count():
            return JsonResponse({'code': 400, 'errmsg': '学号不能重复'})
        #     3.6 用户手机号不能重复
        if User.objects.filter(mobile=phone).count():
            return JsonResponse({'code': 400, 'errmsg': '手机号不能重复'})
        #    3.7 学号只能是12位
        if len(stu_id) != 12:
            return JsonResponse({'code': 400, 'errmsg': '学号输入错误'})
        #  4.数据入库
        # User.objects.create(username=username,password=password,mobile=phone,stu_id=stu_id,stu_class=stu_class,stu_name=name)
        # 密码加密：
        user = User.objects.create_user(username=username, password=password, mobile=phone, stu_id=stu_id,
                                        stu_class=stu_class, stu_name=name)
        # django自带
        from django.contrib.auth import login
        # 登录用户的状态保持
        login(request, user)
        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


# 需求是注册成功后表示用户认证通过；那么此时可以在注册成功后实现状态保持（即注册成功已经登录）状态保持


"""
登录
    
前端：
        当用户把用户名和密码输入完成之后，会点击登录按钮。这个时候前端应该发送一个axios请求
        
后端：
    请求    ：  接收数据，验证数据
    业务逻辑：   验证用户名和密码是否正确，session
    响应    ： 返回JSON数据 0 成功。 400 失败

    POST        /login/
步骤：
    1. 接收数据
    2. 验证数据
    3. 验证用户名和密码是否正确
    4. session
    5. 判断是否记住登录
    6. 返回响应

"""


class LoginView(View):

    def post(self, request):
        # 1. 接收数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 2. 验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        # 确定 我们是根据手机号查询 还是 根据用户名查询

        # USERNAME_FIELD 我们可以根据 修改 User. USERNAME_FIELD 字段
        # 来影响authenticate 的查询
        # authenticate 就是根据 USERNAME_FIELD 来查询
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3. 验证用户名和密码是否正确
        # 我们可以通过模型根据用户名来查询
        # User.objects.get(username=username)

        # 方式2 Django自带的验证
        from django.contrib.auth import authenticate
        # authenticate 传递用户名和密码
        # 如果用户名和密码正确，则返回 User信息
        # 如果用户名和密码不正确，则返回 None
        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})

        # 4. session 状态保持
        from django.contrib.auth import login
        login(request, user)

        # 5. 判断是否记住登录
        if remembered:
            # 记住登录 -- 2周 或者 1个月 具体多长时间 产品说了算
            # none默认两周
            request.session.set_expiry(None)

        else:
            # 不记住登录  浏览器关闭 session过期
            request.session.set_expiry(0)

        # 6. 返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 为了首页显示用户信息
        response.set_cookie('username', username)

        # 必须是登录后 合并
        # from apps.carts.utils import merge_cookie_to_redis
        # response = merge_cookie_to_redis(request, response)

        return response
