# Generated by Django 2.2.1 on 2019-06-14 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0014_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infobox',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='infobox.Infobox'),
        ),
    ]