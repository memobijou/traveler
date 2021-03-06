# Generated by Django 2.2.1 on 2019-11-27 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('Mustahabb', 'Mustahabb'), ('Sunnah', 'Sunnah')], max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupplicationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Bezeichnung')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Beschreibung')),
                ('audio', models.FileField(blank=True, null=True, upload_to='', verbose_name='Audiodatei')),
                ('phonetic_spelling', models.TextField(blank=True, null=True, verbose_name='Lautschrift')),
                ('language', models.CharField(choices=[('Arabisch', 'Arabisch'), ('Deutsch', 'Deutsch'), ('Türkisch', 'Türkisch'), ('Urdu', 'Urdu')], max_length=200, null=True, verbose_name='Typ')),
            ],
        ),
    ]
