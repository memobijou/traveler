# Generated by Django 2.2.1 on 2019-06-10 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0013_auto_20190606_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Beschreibung'),
        ),
    ]
