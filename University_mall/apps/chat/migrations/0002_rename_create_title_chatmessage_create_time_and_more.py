# Generated by Django 4.0.3 on 2022-04-28 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatmessage',
            old_name='create_title',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='chatmessage',
            old_name='update_title',
            new_name='update_time',
        ),
        migrations.RenameField(
            model_name='chatting',
            old_name='create_title',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='chatting',
            old_name='update_title',
            new_name='update_time',
        ),
    ]
