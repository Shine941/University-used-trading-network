from django.db import models
from utils.models import BaseModel


# Create your models here.

# 聊天主要
class Chatting(BaseModel):
    goods_user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='卖家', related_name="chat_user")
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE, verbose_name="商品")
    users = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='买家', related_name="chat_buyer")

    class Meta:
        db_table = 'tb_chatting'
        verbose_name = '聊天主要'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s与%s' % (self.id, self.goods_user.stu_id, self.users.stu_id)


# 聊天主要
class ChatMessage(BaseModel):
    chatting = models.ForeignKey(Chatting, on_delete=models.CASCADE, verbose_name='聊天室')
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='发送者')
    text = models.TextField(verbose_name='聊天内容')

    class Meta:
        db_table = 'tb_chat_message'
        verbose_name = '聊天信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.sender)
