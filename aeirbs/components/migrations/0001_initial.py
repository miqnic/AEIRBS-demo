# Generated by Django 2.2.6 on 2020-05-04 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=15, unique=True)),
                ('device_productID', models.CharField(default='Product ID', max_length=50)),
                ('device_name', models.CharField(max_length=50)),
                ('device_status', models.IntegerField(choices=[(0, 'Connected'), (1, 'Under Maintenance'), (2, 'Needs Maintenance'), (3, 'Inactive')], default=0)),
                ('mac_address', models.CharField(max_length=50)),
                ('floor_location', models.IntegerField(choices=[(1, 'First Floor'), (2, 'Second Floor'), (3, 'Third Floor'), (4, 'Fourth Floor')], default=1)),
                ('device_link', models.CharField(default='Link', max_length=100)),
                ('device_image', models.ImageField(upload_to='component_images')),
                ('last_maintained_datetime', models.DateTimeField(default=None, null=True)),
                ('device_isDeleted', models.BooleanField(default=False)),
                ('last_maintained_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor_type', models.IntegerField(choices=[(0, 'Fire'), (1, 'Flood'), (2, 'Earthquake')])),
                ('sensor_id', models.CharField(max_length=15, unique=True)),
                ('sensor_productID', models.CharField(default='Product ID', max_length=50)),
                ('sensor_name', models.CharField(max_length=50)),
                ('sensor_data', models.CharField(default='Data', max_length=50)),
                ('sensor_voltage', models.CharField(default='Voltage', max_length=50)),
                ('sensor_link', models.CharField(default='Link', max_length=100)),
                ('sensor_image', models.ImageField(upload_to='component_images')),
                ('sensor_isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Device_Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_sensor_id', models.CharField(max_length=10, unique=True)),
                ('sensor_status', models.IntegerField(choices=[(0, 'Connected'), (1, 'Under Maintenance'), (2, 'Needs Maintenance'), (3, 'Inactive')], default=0)),
                ('connectivity_status', models.BooleanField(default=True)),
                ('last_maintained_datetime', models.DateTimeField(default=None, null=True)),
                ('device_sensor_isDeleted', models.BooleanField(default=False)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='components.Device')),
                ('last_maintained_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('sensor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='components.Sensor')),
            ],
        ),
    ]
