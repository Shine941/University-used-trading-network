from django.db import models
from utils.models import BaseModel


# Create your models here.


# 商品类别
class GoodsCategory(BaseModel):
    """商品类别"""
    name = models.CharField(max_length=10, verbose_name='名称')
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父类别')

    class Meta:
        db_table = 'tb_goods_category'
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 商品主要
class Goods(BaseModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='卖家', related_name="goods_user")
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, verbose_name='商品类别')
    name = models.CharField(max_length=150, verbose_name='标题')
    comments = models.IntegerField(default=0, verbose_name='评价数')
    likes = models.IntegerField(default=0, verbose_name='点赞数')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价钱')
    visits = models.IntegerField(default=0, verbose_name='浏览量')
    collect_num = models.IntegerField(default=0, verbose_name='收藏量')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架销售')
    Buyers = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL, verbose_name='买家', related_name="goods_buyer")
    word = models.TextField(verbose_name='文字介绍')
    defaultimg = models.ImageField(verbose_name='默认图片')

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '商品主要'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class GoodsImage(BaseModel):
    """商品图片"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Goods')
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_Goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.goods.name, self.id)


class GoodsVisitCount(BaseModel):
    """商品访问量"""
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    count = models.IntegerField(verbose_name='访问量', default=0)
    date = models.DateField(auto_now_add=True, verbose_name='统计日期')

    class Meta:
        db_table = 'tb_goods_visit'
        verbose_name = '商品访问量'
        verbose_name_plural = verbose_name


