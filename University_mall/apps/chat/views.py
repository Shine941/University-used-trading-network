from django.db.models import Q
from django.shortcuts import render
from django.views import View
# Create your views here.
from apps.chat.models import ChatMessage, Chatting
from apps.goods.models import Goods
from django.http import JsonResponse
from apps.users.models import User


class ChatGoodsView(View):
    def get(self, request, goodsid):
        goodsid = int(goodsid)
        goods = Goods.objects.get(id=goodsid)
        goods_data = {
            'id': goods.id,
            'username': goods.user.username,
            'class': goods.user.stu_class,
            'stuname': goods.user.stu_name,
            'stuid': goods.user.stu_id,
            'useravatar': goods.user.avatar.url,
            'title': goods.name,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'goods': goods_data})


from utils.views import LoginRequiredJSONMixin


class ChatAlertView(LoginRequiredJSONMixin, View):
    def get(self, request):
        chatmessage = []
        user = request.user
        chatroom = user.chat_recever.filter(brecever=False)  # 所有未读消息室
        if chatroom:
            for room in chatroom:
                goodsid = room.goods.id
                buyerid = room.users.id
                chatmessage.append({
                    'title': room.goods.name,
                    'sender': room.goods_user.id,
                    'buyer': room.sender.username,
                    'url': '/chatting.html?q=%d-%d' % (goodsid, buyerid)
                })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'message': chatmessage})


class UreadMesView(LoginRequiredJSONMixin, View):
    def get(self, request, url):
        chatmessage = []
        # 商品id-买家id
        goodsid = int(url.split('-')[0])
        buyerid = int(url.split('-')[1])
        goods = Goods.objects.get(id=goodsid)  # 聊天的商品
        user = request.user
        # 获取聊天室
        if request.user.id == buyerid:  # 我是买家
            # 未读-我的-买家
            chat = Chatting.objects.filter(
                Q(brecever=False) & Q(goods_id=goodsid) & Q(recever_id=user.id) & Q(sender_id=goods.user_id))
        else:  # 我是卖家
            chat = Chatting.objects.filter(
                Q(brecever=False) & Q(goods_id=goodsid) & Q(recever_id=user.id) & Q(sender_id=buyerid))
        if chat:
            chat = chat[0]
            sender = chat.sender
            chat.brecever = True
            messages = user.message_recever.filter(Q(chatting_id=chat.id) & Q(brecever=False))
            if messages:
                # 头像 文档
                for message in messages:
                    message.brecever = True
                    message.save()
                    chatmessage.append({
                        'avatar': sender.avatar.url,
                        'text': message.text,
                    })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'message': chatmessage})
