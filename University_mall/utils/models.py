from django.db import models

class BaseModel(models.Model):
    create_time= models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time= models.DateTimeField(auto_now_add=True,verbose_name="更新时间")

    class Meta:
        abstract = True   # 说明抽象模型类，用于继承使用，数据迁移时不会创建BaseModel的表
