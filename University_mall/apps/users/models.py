from django.db import models
# Create your models here.
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)  # 手机
    stu_id = models.CharField(max_length=12, unique=True)  # 学号
    stu_class = models.CharField(max_length=20, unique=False)  # 班级
    stu_name = models.CharField(max_length=20, unique=False)  # 姓名
    gender = models.CharField(max_length=20, unique=False)  # 性别
    class Meta:  # 修改表名为tb_user，默认是auth_user
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
