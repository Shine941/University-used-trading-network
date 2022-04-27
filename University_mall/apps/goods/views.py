import requests
from django.shortcuts import render

# Create your views here.


# 上传图片代码测试
from fdfs_client.client import Fdfs_client
import base64

# 1.创建客户端
# 2.修改加载配置文件的路径
client = Fdfs_client('utils/fastdfs/client.conf')
# 3.上传图片
# 图片的绝对路径
# client.upload_by_filename('/home/malifei-py/图片/56c30bfc900250e264f5892b31ae89b5_482x264.jpg')
# 3.获取file_id.upload_by_filename上传成功会返回字典数据
'''
{'Group name': 'group1', 'Remote file_id': 'group1/M00/00/00/wKhRgGJmjKWAdYY5ABofhhQ0G0w385.jpg', 
'Status': 'Upload successed.', 
'Local file name': '/home/malifei-py/图片/56c30bfc900250e264f5892b31ae89b5_482x264.jpg',
 'Uploaded size':1.00MB', 'Storage IP': '192.168.81.128'}
'''
# # 64位的保存在本地然后返回地址
# uly='data:image/png;base64,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'
# uly=base64.b64decode(uly)
# client.upload_by_buffer(uly)

from apps.goods.models import Goods, GoodsImage, GoodsVisitCount, GoodsCategory
from django.views import View
from utils.views import LoginRequiredJSONMixin
import json, re
from fdfs_client.client import Fdfs_client
from django.http import JsonResponse
import os, base64

class GoodsCenterView(LoginRequiredJSONMixin, View):
    def post(self, request):
        # request.user来源于中间件，如果是已登录用户。可以直接获取登录用户的模型实例数据
        # 如果不是登录用户，则是匿名用户
        # 1.接受请求
        body_str = request.body.decode()
        body_dict = json.loads(body_str)
        # 2.获取数据
        user_id = request.user.id
        username = body_dict.get('username')
        goods_img = body_dict.get('goods_img')
        goods_title = body_dict.get('goods_title')
        goods_price = body_dict.get('goods_price')
        goods_text = body_dict.get('goods_text')
        goods_category = body_dict.get('goods_category')
        for a in goods_img:
            a = a.split(',')[1]
            # print(a)
            imgdata = base64.urlsafe_b64decode(a)
            file = open('1.jpg', "wb")
            file.write(imgdata)
            file.close()
            file_address = os.getcwd() + '/1.jpg'
            client = Fdfs_client('utils/fastdfs/client.conf')
            name = client.upload_by_filename(file_address)
            img_name = name.get('Remote file_id')
            print(img_name)
        print(goods_category)
        print(goods_text)
        print(goods_title)
        # # 3.验证数据
        # #     3.1都要有
        # #     all里面的元素只要是None就返回false
        # if not all([username, password, phone, name, stu_id, password2, gender]):
        #     return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # #     3.3密码非空
        # #     3.4确认密码和密码一致
        # if password != password2:
        #     return JsonResponse({'code': 400, 'errmsg': '密码与确认密码不一致'})
        # #     3.5 学号不能重复
        # if User.objects.filter(stu_id=stu_id).count():
        #     return JsonResponse({'code': 400, 'errmsg': '学号不能重复'})
        # #     3.6 用户手机号不能重复
        # if User.objects.filter(mobile=phone).count():
        #     return JsonResponse({'code': 400, 'errmsg': '手机号不能重复'})
        # #    3.7 学号只能是12位
        # if len(stu_id) != 12:
        #     return JsonResponse({'code': 400, 'errmsg': '学号输入错误'})
        #  4.数据入库
        # User.objects.create(username=username,password=password,mobile=phone,stu_id=stu_id,stu_class=stu_class,stu_name=name)
        # 密码加密：
        #user = User.objects.create_user(username=username, password=password, mobile=phone, stu_id=stu_id,
        #                                stu_class=stu_class, stu_name=name, gender=gender)
        # 5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
