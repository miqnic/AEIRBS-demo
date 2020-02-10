from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

import serial 
import json

from .models import Device, Sensor, Device_Sensor

# Create your views here.
def getsensordata():
    print("------Reading collection starts now------")
    sr = serial.Serial("COM3",9600)
    st = list(str(sr.readline(),'utf-8'))
    sr.close() 
    print("------Reading collection ends successfully------")
    return float(str(''.join(st[:])))

def home(request):
    if request.user.is_authenticated:
        all_components = Sensor.objects.all()
        all_sensors=Device_Sensor.objects.all()
        fire_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=0, sensor_status=1, device_id__device_status=1)
        flood_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=1, sensor_status=1, device_id__device_status=1)
        earthquake_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=2, sensor_status=1, device_id__device_status=1)
        other_components = Device.objects.all().filter(device_status=1)

        sensor_reading = getsensordata()

        return render(request, 'AEIRBS-Dashboard.html', {'sensor_reading': sensor_reading, 'all_sensors': all_sensors, 'all_components': all_components, 'other_components': other_components, 'fire_components': fire_components, 'flood_components': flood_components, 'earthquake_components': earthquake_components})
    else:
        return render(request, 'AEIRBS-Login.html')

def add_comp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            incident_type = request.POST.get("selectIncidentType")
            component_id = request.POST.get("inputComponentID")
            sensor_type = request.POST.get("selectComponentName")
            location = request.POST.get("selectLocation")
            temp_device = Device.objects.all().first()

            all_sensors = Sensor.objects.all()

            for sensor in sensors:
                if sensor.sensor_id.sensor_name == sensor_type:
                    sensor_type = sensor
                    break

            new_sensor = Device_Sensor.objects.create(
                device_sensor_id=component_id,
                sensor_id=sensor_type,
                floor_location=location,
                sensor_status=1,
                device_id = temp_device,
            )
            new_sensor.save()

            all_components = Sensor.objects.all()
            fire_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=0, sensor_status=1, device_id__device_status=1)
            flood_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=1, sensor_status=1, device_id__device_status=1)
            earthquake_components = Device_Sensor.objects.all().filter(sensor_id__sensor_type=2, sensor_status=1, device_id__device_status=1)
            other_components = Device.objects.all().filter(device_status=1)

            messages.success(request, f'Added sensor {sensor_type} successfully!')
            return HttpResponseRedirect(request, 'home', {'all_components': all_components, 'other_components': other_components, 'fire_components': fire_components, 'flood_components': flood_components, 'earthquake_components': earthquake_components})
    else:
        return render(request, 'AEIRBS-Login.html')