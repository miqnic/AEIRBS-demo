from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Sensor is the type of sensor (i.e. Flame Sensor)
class Sensor(models.Model):
    sensor_id = models.CharField(max_length=10, unique=True)
    sensor_name = models.CharField(max_length=50)
    sensor_type = models.IntegerField()
    sensor_image = models.ImageField(upload_to='component_images')

    def __str__(self):
        return str(self.sensor_id)

# Device is where the Sensors are mounted on. These are the ones that would interpret the data sent by the sensors.
class Device(models.Model):
    device_id = models.CharField(max_length=10, unique=True)
    device_name = models.CharField(max_length=50)
    device_status = models.IntegerField()
    device_image = models.ImageField(upload_to='component_images')
    mac_address = models.CharField(max_length=50)
    floor_location = models.CharField(max_length=50, default="1")

    def __str__(self):
        return str(self.device_id)

# Device-Sensor is the specific sensor that is mounted on a specific device.
class Device_Sensor(models.Model):
    device_sensor_id = models.CharField(max_length=10, unique=True)
    device_id = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING)
    sensor_status = models.IntegerField()
    connectivity_status = models.BooleanField(default=True)
    last_maintained_datetime = models.DateTimeField(null=True, default=None)
    last_maintained_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, default=None)

    def __str__(self):
        return str(self.device_sensor_id)
