from django.db.models import Q
from django.shortcuts import render
# 上传图片代码测试
from fdfs_client.client import Fdfs_client

# 修改加载配置文件的路径
client = Fdfs_client('utils/fastdfs/client.conf')
from apps.goods.models import Goods, GoodsImage, GoodsVisitCount, GoodsCategory
from utils.views import LoginRequiredJSONMixin
import json, re
from fdfs_client.client import Fdfs_client
import os, base64
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login


# ****************************************************新建商品*****
class GoodsCenterView(LoginRequiredJSONMixin, View):
    def post(self, request):
        # request.user来源于中间件，如果是已登录用户。可以直接获取登录用户的模型实例数据
        # 如果不是登录用户，则是匿名用户
        # 1.接受请求
        body_dict = json.loads(request.body.decode())
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

class ConGoodsView(View):
    def delete(self, request):
        print("到这了")
        data = json.loads(request.body.decode())
        if (data):
            print(data)
            print(type(data))
            goods = Goods.objects.get(id=data)
            goods.is_launched = False
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            return JsonResponse({'code':400,'errmsg':'失误'})


class GoodsAllView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        goodsAll = Goods.objects.filter(is_launched=True).order_by('-update_time')
        for goods in goodsAll:
            username = goods.user.username
            goods_data.append({
                'username': username,
                'goodsuser': goods.user.id,
                'useravatar': goods.user.avatar.url,
                'category': goods.category.name,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goodsAll': goods_data})


class OnlineGoodsView(LoginRequiredJSONMixin,View):
    def get(self, request):
        goods_data = []
        goodsOnline = Goods.objects.filter(Q(is_launched=True) & Q(category__parent_id=1)).order_by('-update_time')
        for goods in goodsOnline:
            username = goods.user.username
            goods_data.append({
                'username': username,
                'goodsuser': goods.user.id,
                'useravatar': goods.user.avatar.url,
                'category': goods.category.name,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})


class OfflineGoodsView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        Offline = Goods.objects.filter(Q(is_launched=True) & Q(category__parent_id=2)).order_by('-update_time')
        for goods in Offline:
            username = goods.user.username
            goods_data.append({
                'username': username,
                'goodsuser': goods.user.id,
                'useravatar': goods.user.avatar.url,
                'category': goods.category.name,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})

class MyGoodsView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id)&Q(is_launched=True)).order_by('-update_time')
        for goods in Mygoods:
            goods_data.append({
                'id': goods.id,
                'username': username,
                'useravatar': avatar,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'mygoods': goods_data})

class MySoldView(LoginRequiredJSONMixin,View):
    def get(self,request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id)&Q(is_launched=False)).order_by('-update_time')
        for goods in Mygoods:
            goods_data.append({
                'id': goods.id,
                'username': username,
                'useravatar': avatar,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'mygoods': goods_data})

class MyBoughtView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id)&Q(is_launched=True)).order_by('-update_time')
        for goods in Mygoods:
            goods_data.append({
                'id': goods.id,
                'username': username,
                'useravatar': avatar,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})

class MyCollectView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id)&Q(is_launched=True)).order_by('-update_time')
        for goods in Mygoods:
            goods_data.append({
                'id': goods.id,
                'username': username,
                'useravatar': avatar,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': goods.update_time.date(),
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})