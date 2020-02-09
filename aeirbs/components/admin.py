from django.contrib import admin
from.models import Device, Device_Sensor, Sensor

# Register your models here.

admin.site.register(Device)
admin.site.register(Device_Sensor)
admin.site.register(Sensor)