# Generated by Django 2.2.2 on 2019-10-19 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='place',
        ),
    ]
