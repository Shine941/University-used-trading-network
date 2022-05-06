from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
# websocket请求
from django.db.models import Q

from apps.chat.models import Chatting, ChatMessage
from apps.goods.models import Goods
from apps.users.models import User


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接受这个客户端的连接
        self.accept()
        # 获取群号，获取路由匹配中的
        group = self.scope['url_route']['kwargs'].get("group")
        # 将这个客户端的连接对象加入到某个地方（内存，redis)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        group = self.scope['url_route']['kwargs'].get("group")
        goodsid = int(group)
        goods = Goods.objects.get(id=goodsid)  # 商品
        # self.send("你好")  # 给当前一个人回复 true是买家
        # 通知组内所有的客户端执行xx_oo的方法，在此方法中可以定义人一功能
        print(self.scope.get('path'))
        allmes = message.get('text').split('@#*/')
        senderid = int(allmes[1])  # 发送者id
        thesender = User.objects.get(id=senderid)  # 发送者
        is_buy = ('true' == allmes[2])  # 是否是买家
        buyerid = int(allmes[0])  # 买家id
        buyer = User.objects.get(id=buyerid)  # 买家
        soulder = User.objects.get(id=goods.user_id)  # 卖家
        # 发送：聊天室 商品-买家-发送者
        chatroom = Chatting.objects.filter(Q(goods_id=goodsid) & Q(users_id=buyerid) & Q(sender_id=senderid))
        # 接受：聊天室 商品-买家-接受者
        rechatroom = Chatting.objects.filter(Q(goods_id=goodsid) & Q(users_id=senderid) & Q(recever_id=senderid))
        if rechatroom:
            rechatroom[0].brecever = True
            remessage = ChatMessage.objects.filter(Q(chatting_id=rechatroom[0].id) & Q(brecever=False))
            for mes in remessage:
                mes.brecever = True
                mes.save()
        # 发送者是否是买家
        if is_buy:  # 发送者是买家
            merecever = soulder  # 消息接受者卖家
        else:  # 发送者卖家
            merecever = buyer  # 消息接受者是买家
        if chatroom:  # 有这个房间
            chatroom=chatroom[0]
            chatroom.brecever=False # 发送室没看
            chatroom.save()
        else:
            # 发送：先创建房间再创建消息
            # 创建房间
            chatroom = Chatting.objects.create(
                goods_user=soulder,
                goods=goods,
                users=buyer,
                sender=thesender,
                recever=merecever,
                brecever=False,
            )
        ChatMessage.objects.create(
            chatting=chatroom,
            sender=thesender,
            recever=merecever,
            text=allmes[3],
            brecever=False,
        )
        async_to_sync(self.channel_layer.group_send)(group, {"type": "xx.oo", "message": message})

    def xx_oo(self, event):
        text = event['message']['text']
        self.send(text)  # 给组里面每个人回复

    def websocket_disconnect(self, message):
        # 客户端与服务端断开连接时，自动触发
        group = self.scope['url_route']['kwargs'].get("group")
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()
