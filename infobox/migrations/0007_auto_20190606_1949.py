# Generated by Django 2.2.1 on 2019-06-06 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0006_infobox_infobox'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infobox',
            old_name='infobox',
            new_name='infobox_parent',
        ),
    ]
