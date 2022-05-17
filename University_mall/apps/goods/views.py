from django.db.models import Q
from django.shortcuts import render
# 上传图片代码测试
from fdfs_client.client import Fdfs_client

# 修改加载配置文件的路径
client = Fdfs_client('utils/fastdfs/client.conf')
from apps.goods.models import Goods, GoodsImage, GoodsVisitCount, GoodsCategory
from utils.views import LoginRequiredJSONMixin
import json
from fdfs_client.client import Fdfs_client
import os, base64
from django.views import View
from django.http import JsonResponse


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


# ****************************************************删除商品*****
class ConGoodsView(View):
    def delete(self, request, goodsid):
        print("到这了")
        goods = Goods.objects.get(id=goodsid)
        goods.is_launched = False
        goods.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


# ****************************************************我的商品*****
class MyGoodsView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id) & Q(is_launched=True)).order_by('-update_time')
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
                'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'mygoods': goods_data})


# ****************************************************我的卖出*****
class MySoldView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id) & Q(is_launched=False)).order_by('-update_time')
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
                'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'mygoods': goods_data})


# ****************************************************我的已购*****
class MyBoughtView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id) & Q(is_launched=True)).order_by('-update_time')
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
                'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})


# ****************************************************我的收藏*****
class MyCollectView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        id = request.user.id
        username = request.user.username
        avatar = request.user.avatar.url
        Mygoods = Goods.objects.filter(Q(user_id=id) & Q(is_launched=True)).order_by('-update_time')
        for goods in Mygoods:
            goods_data.append({
                'id': goods.id,
                'username': username,
                'useravatar': avatar,
                'title': goods.name,
                'stuid': goods.user.stu_id,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})

# ****************************************************全部商品*****
class GoodsAllView(LoginRequiredJSONMixin, View):
    def get(self, request):
        goods_data = []
        userid = request.user.id
        goodsAll = Goods.objects.filter(is_launched=True).order_by('-update_time')
        for goods in goodsAll:
            if goods.user_id == userid:
                chaturl = '#'
            else:
                chaturl = '/chatting.html?q=%d-%d' % (goods.id, userid)
            goods_data.append({
                'username': goods.user.username,
                'chaturl': chaturl,
                'useravatar': goods.user.avatar.url,
                'url': '/detail.html?q=%d' % goods.id,
                'category': goods.category.name,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goodsAll': goods_data})


# ****************************************************商品分类*****
class CategoryGoodsView(LoginRequiredJSONMixin, View):
    def get(self, request, category):
        goods_data = []
        category = int(category)
        if category < 3:
            goodsCategory = Goods.objects.filter(Q(is_launched=True) & Q(category__parent_id=category)).order_by(
                '-update_time')
        else:
            goodsCategory = Goods.objects.filter(Q(is_launched=True) & Q(category_id=category)).order_by('-update_time')
        for goods in goodsCategory:
            username = goods.user.username
            if goods.user.id == request.user.id:
                chaturl = '#'
            else:
                chaturl = '/chatting.html?q=%d-%d' % (goods.id, request.user.id)
            goods_data.append({
                'username': username,
                'chaturl': chaturl,
                'goodsuser': goods.user.id,
                'useravatar': goods.user.avatar.url,
                'url': '/detail.html?q=%d' % goods.id,
                'category': goods.category.name,
                'title': goods.name,
                'comments': goods.comments,
                'likes': goods.likes,
                'price': goods.price,
                'collects': goods.collect_num,
                'text': goods.word,
                'defaultimg': goods.defaultimg.url,
                'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})



from haystack.views import SearchView


# ****************************************************搜索商品*****
class SearchGoodsView(LoginRequiredJSONMixin,SearchView):
    def create_response(self):
        # 获取搜索结果
        context = self.get_context()
        goodslist = []
        # 我们该如何知道里面有什么数据呢
        for item in context['page'].object_list:
            # if item.user_id == request.user.id:
            #     chaturl = '/404.html'
            # else:
            #     chaturl = '/chatting.html?q=%d-%d' % (goods.id, request.user.id)
            goodslist.append({
                'id': item.object.id,
                # 'chaturl': chaturl,
                'username': item.object.user.username,
                'useravatar': item.object.user.avatar.url,
                'title': item.object.name,
                'comments': item.object.comments,
                'likes': item.object.likes,
                'price': item.object.price,
                'collects': item.object.collect_num,
                'text': item.object.word,
                'defaultimg': item.object.defaultimg.url,
                'time': str(item.object.update_time.date()) + '  ' + (str(item.object.update_time.time()))[0:8],
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count,
            })
        return JsonResponse(goodslist, safe=False)


# ****************************************************商品细节*****
class DetailView(View):
    def get(self, request, goodsid):
        goodsid = int(goodsid)
        image = []
        goods = Goods.objects.get(id=goodsid)
        images = goods.goodsimage_set.all()
        if goods.user_id == request.user.id:
            chaturl = '#'
        else:
            chaturl = '/chatting.html?q=%d-%d' % (goods.id, request.user.id)
        for img in images:
            image.append(img.image.url)
        goods_data = {
            'id': goods.id,
            'chaturl': chaturl,
            'username': goods.user.username,
            'class': goods.user.stu_class,
            'stuname': goods.user.stu_name,
            'stuid': goods.user.stu_id,
            'useravatar': goods.user.avatar.url,
            'title': goods.name,
            'comments': goods.comments,
            'likes': goods.likes,
            'price': goods.price,
            'collects': goods.collect_num,
            'text': goods.word,
            'images': image,
            'time': str(goods.update_time.date()) + '  ' + (str(goods.update_time.time()))[0:8],
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})
