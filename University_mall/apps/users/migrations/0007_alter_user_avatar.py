# Generated by Django 4.0.3 on 2022-05-03 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='group1/M00/00/00/wKhRgGJwksqAOLOOAB3_ZcFXPe8058.jpg', upload_to='', verbose_name='头像'),
        ),
    ]
