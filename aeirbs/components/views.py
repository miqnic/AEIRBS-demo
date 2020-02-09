from django.shortcuts import render
from .models import Device, Sensor, Device_Sensor

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        fire_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=0, sensor_status=1, device_id__device_status=1)
        flood_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=1, sensor_status=1, device_id__device_status=1)
        earthquake_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=2, sensor_status=1, device_id__device_status=1)
        other_components = Device.objects.all().filter(device_status=1)
        return render(request, 'AEIRBS-Dashboard.html', {'other_components': other_components, 'fire_components': fire_components, 'flood_components': flood_components, 'earthquake_components': earthquake_components})
    else:
        return render(request, 'AEIRBS-Login.html')