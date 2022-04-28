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
# uly='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACcAAAAnCAYAAACMo1E1AAAAAXNSR0IArs4c6QAABaVJREFUWEeNWIty20YM5In2+O+bNp3aeThuk6mt2sqrTftxHklkZwHscQ88puWMRhIfh8UCWOBY/vn0NA/DMJRShmma7MP/OMdjtxuH8/lsn3me7f7dbmeX8X8cRzuHg+vgPO7xe5e1dH0+cz5PdU08Zza+Hf6Y8QPHxcWFGcH/0+lkRrA4PqfTuYKuiAMYjen57CDWIhB1ennGAfFjzys4ACM4MERwOHc8nuriGQQZopNkU0FwXazZACilYVYBlr+e9kYbQ8NQMXz4j4XJnLKkYMC6GtVrjArTQtdmZBD2FXMEpyFk3uD7/4YV4OhkBlaK5yZzkXkNQHAcNua5ZRT/K3PwhslLIwoOCcuD4cphzOFeWHZWhoHfnuOoH6zl6/k5v08Kgl5pjtAwAU8TF2yrjvdlttqCgBLMtA+MwZSz5WEfG3C42QoiV08t5fDKZcblo3ewIJRxzU2E1Zh3HOAl2FlCOY4eel8DUZqH8vfHR3tENUtZIO3nBE5hZnA9Fo2u5mgjMU0uVQyrOQcRZjGsqoVCW0p4GzlCQ6FL4rLn0uACDThY+wyNM2ZYka3Qg4CcvyiW8i2YW1eYe1pVP2JShRQphHyJnEHV4fccDI/RPQhu1+SUu6OibB1BQFrE/jzsZ3iJamVLyoVhGRIgtFKtxizRZ+suZiCYoyGLBvIn2lg3aYNhTS0D9/WwXxVEr0C25KNEku+0D8fvyno4Bu1gDtNZ7Rh6zX5/edpbb728vKwKTZEk9YsWsZoCkZeesWVFUTVL9ct/nyIyCgDPEByLsgnt58e9FcTV1VUzTTAHGOqlzAUY8yYA9nKIOnk8nYYSk0kT8igqtknYqZPRYf9gzDFnWM5qyHVuEUwCJQv13sg3K4wIpeVRKcPZtCuJiUwhHDpwRx3LHu/vrSA40tDTnHcYoXrAaZzFYDdNs4XRQoVQh8CSc+0q6gRtcyIqH/c+bOJEPpS94/FYL3MYQLJBw/AsclbZ7YWOTZ6h007EUPKcDa+P994hSOUWQBVoLRDIxBQTL+/R/NRzOljkNMk92u69f//gSjS5HlnoosnX3Nq54tfxG0Ibya3lAZDKRnaI1c8qVSJUqtgOy93teyuIrd7KBXzmasdo7SoKjCAsfOE4dTCvwXtpnwRYdN68/tWkJFdr41WwmcOJfKMxAyctruoZNdDnpGZaVhsZnIF+dfPOmOt1AH14OvkwarmwK5ZnGh6Cs5EyBgYrCi/xwcYAkZhsT8WZxVmuf3lrzFEmenlg4SG4ccexrG4RCcJCGI5WYAQHoDKwahotY7tvI6sI//zytYHT/KmFIO1oQvvpNG8r+TgPodUBQfPLwMh+N4cR9y77iZj1Xvxwbb+oU3kTUhM2Ns0qB2S7KYzK67I5spBxxJKwU+9gk5vymjp45scXNzXntOlmw8panixUIjLrPRXQfs28tXkwjir+L396Zczl9qXgjBnbKmlGLsNiL0+/N8k0VS+NP4u4FQQW/+6wGeCyRmnj5/MZVOtO/9+WWpSb69v6ImfLuIYt90+CqeUvRbQFbEuIs2PGHE4i5jbvxzsSdo3a5ENMe+CyDOWJJl/P7Yu5rvroInzt4Ng7CQ4XCcyudVqXgtD2tkrs0K7cP6sS2FssH8mUvfL25nauTXzysdmKA1uzoQwjdk0cNmWjk9no9V5lQl936HDACfj5+XmVBeXuzV3NOTWoSWrVHOpPRln68Bgf6lTjuWx6MA9qAWU14HqqmeXDu99Wu69uWDC3RSdhjrLVkO0clp7EbBWJ6mG1v//wu4HL7avxMvQNUwj7nr5mzfrUA7AV9h6bFdzhwV/k5CokC/bNwTK2crmq2Bfp4FafZpVq/9V2uCLoy6PvIbL3OefmYG8rb/5rWM2vXbVSe5Ez+1+fHFwuhlVoUL1pJ68O0fiqBckzPUY1Qtnmv57S3P7iX1u3AAAAAElFTkSuQmCC'
# uly=base64.b64decode(uly)
# client.upload_by_buffer(uly)

from apps.goods.models import Goods, GoodsImage, GoodsVisitCount, GoodsCategory
from django.views import View
from utils.views import LoginRequiredJSONMixin
import json, re
from fdfs_client.client import Fdfs_client
from django.http import JsonResponse
import os, base64
from collections import OrderedDict


# ****************************************************新建商品*****
class GoodsCenterView(LoginRequiredJSONMixin, View):
    def post(self, request):
        # request.user来源于中间件，如果是已登录用户。可以直接获取登录用户的模型实例数据
        # 如果不是登录用户，则是匿名用户
        # 1.接受请求
        body_str = request.body.decode()
        body_dict = json.loads(body_str)
        # 2.获取数据
        goods_img = body_dict.get('goods_img')
        goods_title = body_dict.get('goods_title')
        goods_price = body_dict.get('goods_price')
        goods_text = body_dict.get('goods_text')
        goods_price = float(goods_price)
        goods_category = int(body_dict.get('goods_category'))
        category = GoodsCategory.objects.get(id=goods_category)
        # 设置默认图片
        b = goods_img[0]
        defimg = b.split(',')[1]
        imgdata = base64.urlsafe_b64decode(defimg)
        file = open('1.jpg', "wb")
        file.write(imgdata)
        file.close()
        file_address = os.getcwd() + '/1.jpg'
        client = Fdfs_client('utils/fastdfs/client.conf')
        name = client.upload_by_filename(file_address)
        img_name = name.get('Remote file_id')
        goods = Goods(
            name=goods_title,
            price=goods_price,
            word=goods_text,
            defaultimg=img_name,
        )
        goods.category = category
        goods.user = request.user
        goods.save()
        for a in goods_img:
            a = a.split(',')[1]
            imgdata = base64.urlsafe_b64decode(a)
            file = open('1.jpg', "wb")
            file.write(imgdata)
            file.close()
            file_address = os.getcwd() + '/1.jpg'
            client = Fdfs_client('utils/fastdfs/client.conf')
            name = client.upload_by_filename(file_address)
            img_name = name.get('Remote file_id')
            img = GoodsImage(
                image=img_name
            )
            img.goods = goods
            img.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class GetGoodsAllView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        goodsAll = Goods.objects.filter(is_launched=True).order_by('-update_title')
        for goods in goodsAll:
            username = goods.user.username
            goods_data.append({
                'username': username,
                'useravatar': goods.user.avatar.url,
                'category': goods.category.name,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_title,
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goodsAll': goods_data})
