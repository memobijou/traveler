# Generated by Django 2.2.1 on 2019-05-19 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0002_infobox'),
    ]

    operations = [
        migrations.AddField(
            model_name='infobox',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='infobox.Category', verbose_name='Kategorie'),
        ),
    ]