from django.db import models
from django.contrib.auth.models import User

# Create your models here.
INCIDENT_TYPE = [
    (0, 'Earthquake'),
    (1, 'Fire'),
    (2, 'Flood')
]
STATUS = [
    (0, 'Connected'),
    (1, 'Under Maintenance'),
    (2, 'Needs Maintenance'),
    (3, 'Inactive')
]
FLOOR_LOCATIONS = [
    (1, 'First Floor'),
    (2, 'Second Floor'),
    (3, 'Third Floor'),
    (4, 'Fourth Floor'),
]
DEVICE_TYPE = [
    (0, 'Universal'),
    (1, 'Earthquake'),
    (2, 'Fire'),
    (3, 'Flood')
]

DEFAULT_IMAGE = "component_images\default.png"

class Floor(models.Model):
    floor_identifier = models.CharField(max_length=3)
    floor_description = models.CharField(max_length=20)

    def __str__(self):
        return str(self.floor_description)

class Alarm(models.Model):
    incident = models.IntegerField(choices=INCIDENT_TYPE)
    announcement = models.TextField()

    def __str__(self):
        if self.incident == 0:
            return str('Earthquake')
        elif self.incident == 1:
            return str('Fire')
        else:
            return str('Flood')

# Sensor is the type of sensor (i.e. Flame Sensor)
class Sensor(models.Model):
    sensor_type = models.IntegerField(choices=INCIDENT_TYPE)
    sensor_id = models.CharField(max_length=20, unique=True)
    sensor_productID = models.CharField(max_length=50, default="Product ID")
    sensor_name = models.CharField(max_length=50)
    sensor_data = models.CharField(max_length=50,  default="Data")
    sensor_voltage = models.CharField(max_length=50,  default="Voltage")
    sensor_link = models.CharField(max_length=100,  default="Link")
    sensor_image = models.ImageField(upload_to='component_images')

    sensor_isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sensor_id)

# Device is where the Sensors are mounted on. These are the ones that would interpret the data sent by the sensors.
class Device(models.Model):
    device_id = models.CharField(max_length=20, unique=True)
    device_productID = models.CharField(max_length=50, default="Product ID")
    device_name = models.CharField(max_length=50)
    device_status = models.IntegerField(choices=STATUS, default=3)
    port_number = models.CharField(max_length=50)
    floor_location = models.CharField(max_length=3, default='1')
    device_link = models.CharField(max_length=100, default="Link")
    device_image = models.ImageField(upload_to='component_images')
    last_maintained_datetime = models.DateTimeField(null=True, default=None)
    last_maintained_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, default=None)
    device_type = models.IntegerField(default=0)

    device_isDeleted = models.BooleanField(default=False)
    device_maxedOut = models.BooleanField(default=False)

    def __str__(self):
        return str(self.device_id)

# Device-Sensor is the specific sensor that is mounted on a specific device.
class Device_Sensor(models.Model):
    device_sensor_id = models.CharField(max_length=20)
    device_id = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.DO_NOTHING)
    sensor_status = models.IntegerField(choices=STATUS, default=0)
    connectivity_status = models.BooleanField(default=True)
    last_maintained_datetime = models.DateTimeField(null=True, default=None)
    last_maintained_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, default=None)

    device_sensor_isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.device_sensor_id)