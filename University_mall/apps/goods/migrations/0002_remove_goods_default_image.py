# Generated by Django 4.0.3 on 2022-04-27 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='default_image',
        ),
    ]