# Generated by Django 2.2.1 on 2019-10-21 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0015_auto_20190614_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='infobox',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Audiodatei'),
        ),
    ]
