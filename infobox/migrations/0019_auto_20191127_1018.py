# Generated by Django 2.2.1 on 2019-11-27 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0018_auto_20191029_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infobox',
            name='audio',
        ),
        migrations.RemoveField(
            model_name='infobox',
            name='type',
        ),
    ]