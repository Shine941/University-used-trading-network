from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

"""
前端
     拼接一个 url 。然后给 img 。img会发起请求
     url=http://mp-meiduo-python.itheima.net/image_codes/ca732354-08d0-416d-823b-14b1d77746d2/
     url=http://ip:port/image_codes/uuid
后端
    请求              接收路由中的 uuid
    业务逻辑          生成图片验证码和图片二进制。通过redis把图片验证码保存起来
    响应              返回图片二进制

    路由：     GET     image_codes/uuid/
    步骤：         
            1. 接收路由中的 uuid
            2. 生成图片验证码和图片二进制
            3. 通过redis把图片验证码保存起来
            4. 返回图片二进制
"""
# Create your views here.
from django.views import View


class ImageCodeView(View):
    def get(self, request, uuid):
        # 1.接过路由中的uuid
        # 2.生成图片验证码和图片二进制
        from libs.captcha.captcha import captcha
        # text是图片文本内容；image是图片二进制
        text, image = captcha.generate_captcha()
        # 3. 通过redis把图片验证码保存起来
        # 3.1 进行redis的连接
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')  # 6号库
        # 3.2 指令操作
        # name, time, value  120秒过期
        redis_cli.setex(uuid, 120, text)
        # 4. 返回图片二进制
        # 因为图片是二进制 我们不能返回JSON数据
        # content_type=响应体数据类型
        # content_type 的语法形式是： 大类/小类
        # content_type (MIME类型)
        # 图片： image/jpeg , image/gif, image/png
        return HttpResponse(image, content_type='image/jpeg')


'''
前端
            当用户输入完 手机号，图片验证码之后，前端发送一个axios请求
后端
    请求：     接收请求，获取请求参数（路由有手机号， 用户的图片验证码和UUID在查询字符串中）
    业务逻辑：  验证参数， 验证图片验证码， 生成短信验证码，保存短信验证码，发送短信验证码
    响应：     返回响应
            {‘code’:0,'errmsg':'ok'}
    路由：     GET     sms_codes/18310820644/?image_code=knse&image_code_id=b7ef98bb-161b-437a-9af7-f434bb050643
'''


# 短信验证码
class SmsCodeView(View):
    def get(self, request, mobile):
        # 1. 获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2. 验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3. 验证图片验证码
        # 3.1 连接redis
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # 3.2 获取redis数据
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        # 3.3 对比
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 提取发送短信的标记，看看有没有
        send_flag = redis_cli.get('send_flag_%s' % mobile)
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '不要频繁发送短信'})
        # 4. 生成短信验证码
        from random import randint
        sms_code = '%06d' % randint(0, 999999)  # 6位

        # 管道 3步
        # ① 新建一个管道
        pipeline = redis_cli.pipeline()
        # ② 管道收集指令
        # 5. 保存短信验证码
        pipeline.setex(mobile, 300, sms_code)
        # 添加一个发送标记.有效期 60秒 内容是什么都可以
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        # ③ 管道执行指令
        pipeline.execute()

        # # 5. 保存短信验证码
        # redis_cli.setex(mobile,300,sms_code)
        # # 添加一个发送标记.有效期 60秒 内容是什么都可以
        # redis_cli.setex('send_flag_%s'%mobile,60,1)

        # 6. 发送短信验证码
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # from celery_tasks.sms.tasks import celery_send_sms_code
        # # delay 的参数 等同于 任务（函数）的参数
        # celery_send_sms_code.delay(mobile,sms_code)

        # 7. 返回响应
        return JsonResponse({'code':0,'errmsg':'ok'})
