# Generated by Django 4.0.3 on 2022-04-26 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_stu_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='', upload_to='', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=20, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=11, unique=True, verbose_name='手机'),
        ),
        migrations.AlterField(
            model_name='user',
            name='stu_class',
            field=models.CharField(max_length=20, verbose_name='班级'),
        ),
        migrations.AlterField(
            model_name='user',
            name='stu_id',
            field=models.CharField(max_length=12, unique=True, verbose_name='学号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='stu_name',
            field=models.CharField(max_length=20, verbose_name='姓名'),
        ),
    ]
