# Generated by Django 2.2.6 on 2020-04-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('components', '0031_auto_20200420_1037'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='device_isDeleted',
        ),
        migrations.RemoveField(
            model_name='device_sensor',
            name='device_sensor_isDeleted',
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='sensor_isDeleted',
        ),
        migrations.AddField(
            model_name='device',
            name='device_isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='device_sensor',
            name='device_sensor_isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_isActive',
            field=models.BooleanField(default=True),
        ),
    ]