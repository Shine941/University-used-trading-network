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
                    'sender': room.sender.username,
                    'buyer': room.users.username,
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
        user = request.user  # 用户
        tag = True  # 我是买家
        # 获取未读消息聊天
        if request.user.id == buyerid:  # 我是买家
            # 未读-我的-买家
            chat = Chatting.objects.filter(
                Q(brecever=False) & Q(goods_id=goodsid) & Q(recever_id=user.id) & Q(sender_id=goods.user_id))
        else:  # 我是卖家
            tag = False  # 我是卖家
            # 未读-商品-我的-卖家
            chat = Chatting.objects.filter(
                Q(brecever=False) & Q(goods_id=goodsid) & Q(recever_id=user.id) & Q(sender_id=buyerid))
        if chat:  # 有未读消息室
            chat = chat[0]
            sender = chat.sender
            chat.brecever = True
            chat.save()
            # 发送者是我吗-发送头像-发送具体信息
            messages = user.message_recever.filter(Q(chatting_id=chat.id) & Q(brecever=False))
            if messages:
                # 是我吗-头像-文档
                for message in messages:
                    # 已读
                    message.brecever = True
                    message.save()
        messages = ChatMessage.objects.filter(Q(sender_id=request.user.id) | Q(recever_id=request.user.id)).order_by(
            'update_time')
        for message in messages:
            if message.chatting.goods_id == goodsid:
                chatmessage.append({
                    'tag': message.sender_id == request.user.id,  # 是我的发送吗
                    'avatar': message.sender.avatar.url,
                    'text': message.text,
                })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'message': chatmessage})


class OnreadMesView(LoginRequiredJSONMixin, View):
    def get(self, request, url):
        # 商品id-买家id
        goodsid = int(url.split('-')[0])
        buyerid = int(url.split('-')[1])
        goods = Goods.objects.get(id=goodsid)  # 聊天的商品
        user = request.user  # 用户
        # 获取未读消息聊天
        if request.user.id == buyerid:  # 我是买家
            # 未读-我的-买家
            chat = Chatting.objects.filter(
                Q(brecever=False) & Q(goods_id=goodsid) & Q(recever_id=user.id) & Q(sender_id=goods.user_id))
        else:  # 我是卖家
            tag = False  # 我是卖家
            # 未读-商品-我的-卖家
            chat = Chatting.objects.filter(
                Q(brecever=False) & Q(goods_id=goodsid) & Q(recever_id=user.id) & Q(sender_id=buyerid))
        if chat:  # 我有未读消息室
            chat = chat[0]
            chat.brecever = True
            chat.save()
            # 发送者是我吗-发送头像-发送具体信息
            messages = user.message_recever.filter(Q(chatting_id=chat.id) & Q(brecever=False))
            if messages:
                # 是我吗-头像-文档
                for message in messages:
                    # 已读
                    message.brecever = True
                    message.save()
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class MyChatView(LoginRequiredJSONMixin, View):
    def get(self, request):
        chatmessage = []
        user = request.user
        chatroom = Chatting.objects.filter(recever_id=user.id).order_by('-update_time')
        if chatroom:
            for room in chatroom:
                goodsid = room.goods.id
                buyerid = room.users.id
                chatmessage.append({
                    'tag': room.goods.user_id == user.id,  # 是不是我的商品
                    'title': room.goods.name,
                    'solder': room.goods.user.username,  # 发送者
                    'time': str(room.update_time.date()) + '  ' + (str(room.update_time.time()))[0:8],  # 时间
                    'buyer': room.users.username,  # 买家
                    'url': '/chatting.html?q=%d-%d' % (goodsid, buyerid)
                })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'message': chatmessage})


