# Generated by Django 4.0.3 on 2022-04-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_avatar_alter_user_gender_alter_user_mobile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='', verbose_name='头像'),
        ),
    ]
