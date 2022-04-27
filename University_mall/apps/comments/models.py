from django.db import models
from utils.models import BaseModel


# Create your models here.
# 商品评论
class GoodsComment(BaseModel):
    goods = models.ForeignKey('goods.Goods', on_delete=models.CASCADE, verbose_name='商品')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='评论人')
    text = models.TextField(verbose_name='评论文字')

    class Meta:
        db_table = 'tb_Goods_comment'
        verbose_name = '商品评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.goods.name, self.id)
