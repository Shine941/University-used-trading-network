from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync


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
        # self.send("你好")  # 给当前一个人回复
        # 通知组内所有的客户端执行xx_oo的方法，在此方法中可以定义人一功能
        async_to_sync(self.channel_layer.group_send)(group, {"type": "xx.oo", "message": message})

    def xx_oo(self, event):
        text = event['message']['text']
        self.send(text)  # 给组里面每个人回复

    def websocket_disconnect(self, message):
        # 客户端与服务端断开连接时，自动触发
        group = self.scope['url_route']['kwargs'].get("group")
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()
