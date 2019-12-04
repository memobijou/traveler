# Generated by Django 2.2.1 on 2019-11-27 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infobox', '0019_auto_20191127_1018'),
        ('supplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplication',
            name='infobox',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='infobox.Infobox', verbose_name='Infobox'),
        ),
        migrations.AlterField(
            model_name='supplication',
            name='type',
            field=models.CharField(blank=True, choices=[('Mustahabb', 'Mustahabb'), ('Sunnah', 'Sunnah')], max_length=200, null=True, verbose_name='Art'),
        ),
        migrations.AlterField(
            model_name='supplicationdata',
            name='language',
            field=models.CharField(choices=[('Arabisch', 'Arabisch'), ('Deutsch', 'Deutsch'), ('Türkisch', 'Türkisch'), ('Urdu', 'Urdu')], max_length=200, null=True, verbose_name='Sprache'),
        ),
    ]