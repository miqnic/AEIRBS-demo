from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from reports.models import AuditLogs

import serial 
import json
import datetime

from .models import Device, Sensor, Device_Sensor, FLOOR_LOCATIONS, INCIDENT_TYPE, STATUS, DEFAULT_IMAGE

# Create your views here.
 
# Connect to Arduino through COM3 port
def getArduinoData():
    port_stream = serial.Serial("COM3",9600)
    ard_data = list(str(port_stream.readline(),'utf-8'))
    port_stream.close() 
    return float(str(''.join(ard_data[:])))

def add_component(request):
    if request.user.is_authenticated:
        context = {}
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)

        return render(request, 'DASHBOARD-AddComponent.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def fire_components(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['fire_components'] = Device_Sensor.objects.all().filter(sensor_id__sensor_type=0, device_sensor_isDeleted=False)
      
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        return render(request, 'DASHBOARD-FireComponents.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')
        
def earthquake_components(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['earthquake_components'] = Device_Sensor.objects.all().filter(sensor_id__sensor_type=2, device_sensor_isDeleted = False)
       
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        return render(request, 'DASHBOARD-EarthquakeComponents.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def flood_components(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['flood_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted=False)
       
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        return render(request, 'DASHBOARD-FloodComponents.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def devices(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE
        context['status'] = STATUS

        context['sensor_reading'] = " "#getArduinoData()

        return render(request, 'DASHBOARD-Devices.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def sensors(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        return render(request, 'DASHBOARD-Sensors.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def add_device(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            add_deviceName = request.POST.get("addDeviceName")
            add_deviceProductID = request.POST.get("addDeviceProductID")
            add_deviceMacAddress = request.POST.get("addDeviceMacAddress")
            add_deviceFloorLocation = request.POST.get("addDeviceFloorLocation")
            add_deviceLink = request.POST.get("addDeviceLink")
            add_deviceImage = request.FILES.get("addDeviceImage")
            
            if add_deviceImage == None:
                add_deviceImage = DEFAULT_IMAGE
        
            id = add_deviceName[0:5]
            count = (Device.objects.filter(device_name__contains=id.upper())).count()
            add_deviceID = "DEV-" + id.upper() + "0" + str(count + 1)

            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            add_device = Device.objects.create(
                device_id = add_deviceID,
                device_productID = add_deviceProductID,
                device_name = add_deviceName,
                mac_address = add_deviceMacAddress,
                floor_location = add_deviceFloorLocation,
                device_link = add_deviceLink,
                device_image = add_deviceImage,
            )
            add_device.save()

            add_log = AuditLogs.objects.create(
                log_id = "CL0" + str(all_userLogs + 1),
                activity = "Add Device",
                username = request.user,
                audit_details = str(request.user) + " added component " + str(add_deviceID) + " to the system.",
                audit_type = 0
            )
            add_log.save()
            
            messages.success(request, f'Added component {add_deviceID} successfully!')
            return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html')

def add_sensor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            add_sensorType = request.POST.get("addSensorIncidentType")
            add_sensorProductID = request.POST.get("addSensorProductID")
            add_sensorName = request.POST.get("addSensorName")
            add_sensorData = request.POST.get("addSensorData")
            add_sensorVoltage = request.POST.get("addSensorVoltage")
            add_sensorLink = request.POST.get("addSensorLink")
            add_sensorImage = request.FILES.get("addSensorImage")
            
            if add_sensorImage == None:
                add_sensorImage = DEFAULT_IMAGE
          
            id = add_sensorName[0:3]
            
            if add_sensorType == "0":
                type = "FR"
            elif add_sensorType == "1":
                type = "FL"
            else:
                type = "EQ"

            count = Sensor.objects.filter(sensor_type = add_sensorType).count()

            add_sensorID = type + "SEN-"  + id.upper() + "-0" + str(count + 1)

            all_sensors = Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            isExisting = False
            for sensor in all_sensors:
                if sensor.sensor_name.upper() == add_sensorName.upper():
                    isExisting = True
                    break

            if isExisting:
                messages.error(request, f'Sensor {add_sensorID} is already in the system!')   
            else:
                add_sensor = Sensor.objects.create(
                    sensor_type = add_sensorType,
                    sensor_id = add_sensorID,
                    sensor_productID = add_sensorProductID,
                    sensor_name = add_sensorName,
                    sensor_data = add_sensorData,
                    sensor_voltage = add_sensorVoltage,
                    sensor_link = add_sensorLink,
                    sensor_image = add_sensorImage,
                )
                add_sensor.save()
                
                add_log = AuditLogs.objects.create(
                    log_id = "CL0" + str(all_userLogs + 1),
                    activity = "Add Sensor",
                    username = request.user,
                    audit_details = str(request.user) + " added sensor " + str(add_sensorID) + " to the system.",
                    audit_type = 0
                )
                add_log.save()

                messages.success(request, f'Added sensor {add_sensorID} successfully!')      
            return redirect('earthquake_components')    
    else:
        return render(request, 'AEIRBS-Login.html')

def add_comp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            all_devices = Device.objects.all()
            all_sensors = Sensor.objects.all()

            add_deviceID = request.POST.get("addDeviceID")
            add_sensorID = request.POST.get("addSensorID")

            deviceID = Device.objects.filter(device_id = add_deviceID).first()
            sensorID = Sensor.objects.filter(sensor_id = add_sensorID).first()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for device in all_devices:
                if device.device_id == add_deviceID:
                    floor_location = device.floor_location
                    break

            for sensor in all_sensors:
                if sensor.sensor_id == add_sensorID:
                    if sensor.sensor_type == 0:
                        sensor_typeIndex = 0
                        sensor_type = "FR"
                    elif sensor.sensor_type == 1:
                        sensor_typeIndex = 1
                        sensor_type = "FL"
                    else:
                        sensor_typeIndex = 2
                        sensor_type = "EQ"
                    break
            
            add_device_sensorID = "DS-" + sensor_type + "0" + str(floor_location) + "0"

            count = Device_Sensor.objects.filter(sensor_id__sensor_type__contains = sensor_typeIndex).count()

            add_device_sensorID += str(count + 1)

            add_component = Device_Sensor.objects.create(
                device_sensor_id = add_device_sensorID,
                device_id = deviceID,
                sensor_id = sensorID,
            )
            add_component.save()

            add_log = AuditLogs.objects.create(
                log_id = "CL0" + str(all_userLogs + 1),
                activity = "Add Connection",
                username = request.user,
                audit_details = str(request.user) + " connected sensor " + str(sensorID) + " to " + str(deviceID) + ".",
                audit_type = 0
            )
            add_log.save()

            messages.success(request, f'Connected sensor {sensorID} to {deviceID} successfully!')
            return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_device(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            edit_deviceID = request.POST.get("editDeviceID")
            edit_deviceName = request.POST.get("editDeviceName")
            edit_deviceProductID = request.POST.get("editDeviceProductID")
            edit_deviceMacAddress = request.POST.get("editDeviceMacAddress")
            edit_deviceFloorLocation = request.POST.get("editDeviceFloorLocation")
            edit_deviceLink = request.POST.get("editDeviceLink")
            edit_deviceImage = request.FILES.get("editDeviceImage")

            all_devices = Device.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for device in all_devices:
                if device.device_id == edit_deviceID:
                    if edit_deviceImage == None:
                        edit_deviceImage = device.device_image
                    device.device_id = edit_deviceID
                    device.device_name = edit_deviceName
                    device.device_productID = edit_deviceProductID
                    device.mac_address = edit_deviceMacAddress
                    device.floor_location = edit_deviceFloorLocation
                    device.device_link = edit_deviceLink
                    device.device_image = edit_deviceImage
                    device.save()

                    add_log = AuditLogs.objects.create(    
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Edit Device",
                        username = request.user,
                        audit_details = str(request.user) + " updated device " + edit_deviceID + "'s details.",
                        audit_type = 0
                    )
                    add_log.save()
                    
                    messages.success(request, f'Updated {edit_deviceID} successfully!')
                    return redirect('devices')
           
            messages.error(request, f'Device {edit_deviceID} not found!')
            return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_sensor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            sensorID = request.POST.get("editSensorID")
            edit_sensorType = request.POST.get("editSensorIncidentType")
            edit_sensorProductID = request.POST.get("editSensorProductID")
            edit_sensorName = request.POST.get("editSensorName")
            edit_sensorData = request.POST.get("editSensorData")
            edit_sensorVoltage = request.POST.get("editSensorVoltage")
            edit_sensorLink = request.POST.get("editSensorLink")
            edit_sensorImage = request.FILES.get("editSensorImage")
                      
            id = edit_sensorName[0:3]

            if edit_sensorType == "0":
                type = "FR"
            elif edit_sensorType == "1":
                type = "FL"
            else:
                type = "EQ"

            edit_sensorID = type + "SEN-"  + id.upper() + "-0" + str(Sensor.objects.filter(sensor_type = edit_sensorType).count() + 1)

            all_components = Device_Sensor.objects.all()
            all_sensors = Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            counter = 0

            for component in all_components:
                if component.sensor_id.sensor_id == sensorID:
                    counter += 1
                    print(Device_Sensor.objects.filter(sensor_id__sensor_type = edit_sensorType).count() + 1)
                    id = "DS-" + type + "0" + str(component.device_id.floor_location) + "0" + str(Device_Sensor.objects.filter(sensor_id__sensor_type = edit_sensorType).count() + counter)
                    component.device_sensor_id = id
                    component.save()
                    continue

            for sensor in all_sensors:
                if sensor.sensor_id == sensorID:
                    if edit_sensorImage == None:
                        edit_sensorImage = sensor.sensor_image
                    sensor.sensor_id = edit_sensorID
                    sensor.sensor_type = edit_sensorType
                    sensor.sensor_name = edit_sensorName
                    sensor.sensor_productID = edit_sensorProductID
                    sensor.sensor_data = edit_sensorData
                    sensor.sensor_volatage = edit_sensorVoltage
                    sensor.sensor_link = edit_sensorLink
                    sensor.sensor_image = edit_sensorImage
                    sensor.save()

                    add_log = AuditLogs.objects.create(    
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Edit Sensor",
                        username = request.user,
                        audit_details = str(request.user) + " updated sensor " + sensorID + "'s details.",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Updated {sensorID} successfully!')
                    return redirect('sensors')
           
            messages.error(request, f'Sensor {sensorID} not found!')
            return redirect('sensors')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_comp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            componentID = request.POST.get("editComponentID")
            #sensorID = request.POST.get("editComponentSensorID")
            deviceID = request.POST.get("editComponentDeviceID")
            edit_deviceID = Device.objects.filter(device_id = deviceID).first()

            all_components = Device_Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for component in all_components:
                print(component.device_sensor_id)
                if component.device_sensor_id == componentID:
                    component.device_id = edit_deviceID
                    component.save()

                    add_log = AuditLogs.objects.create(    
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Edit Component",
                        username = request.user,
                        audit_details = str(request.user) + " updated component " + componentID + "'s details.",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Updated {componentID} successfully!')
                    if component.sensor_id.sensor_type == 0:
                        return redirect('fire_components')
                    elif component.sensor_id.sensor_type == 1:
                        return redirect('flood_components')
                    else:
                        return redirect('earthquake_components')

            messages.error(request, f'Component {componentID} not found!')
            return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html')

def del_device(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            delete_deviceID = request.POST.get("deleteDeviceID")

            all_devices = Device.objects.all()
            all_components = Device_Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for device in all_devices:
                if device.device_id == delete_deviceID:
                    device.device_isDeleted = True
                    device.save()

                    for component in all_components:
                        if component.device_id.device_id == device.device_id:
                            component.device_sensor_isDeleted = True
                            component.save()

                    add_log = AuditLogs.objects.create(    
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Delete Device",
                        username = request.user,
                        audit_details = str(request.user) + " deleted device " + delete_deviceID + " from the system.",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Deleted device {delete_deviceID} successfully!')
                    return redirect('devices')

            messages.error(request, f'Sensor {delete_deviceID} not found!')
            return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')

def del_sensor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            delete_sensorID = request.POST.get("deleteSensorID")

            all_sensors = Sensor.objects.all()
            all_components = Device_Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for sensor in all_sensors:
                if sensor.sensor_id == delete_sensorID:
                    sensor.sensor_isDeleted = True
                    sensor.save()
                    
                    print("sensor " + sensor.sensor_id + " deleted")

                    for component in all_components:
                        if component.sensor_id.sensor_id == sensor.sensor_id:
                            component.device_sensor_isDeleted = True
                            component.save()

                    add_log = AuditLogs.objects.create(    
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Delete Sensor",
                        username = request.user,
                        audit_details = str(request.user) + " deleted senser " + delete_sensorID + " from the system.",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Deleted sensor {delete_sensorID} successfully!')
                    return redirect('sensors')

            messages.error(request, f'Sensor {delete_sensorID} not found!')
            return redirect('sensors')
    else:
        return render(request, 'sensors')

def del_comp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            delete_componentID = request.POST.get("deleteComponentID")

            all_components = Device_Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for component in all_components:
                if component.device_sensor_id == delete_componentID:
                    component.device_sensor_isDeleted = True
                    component.save()

                    add_log = AuditLogs.objects.create(    
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Delete Component",
                        username = request.user,
                        audit_details = str(request.user) + " deleted component " + delete_componentID + " from the system.",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Deleted component {delete_componentID} successfully!')
                    if component.sensor_id.sensor_type == 0:
                        return redirect('fire_components')
                    elif component.sensor_id.sensor_type == 1:
                        return redirect('flood_components')
                    else:
                        return redirect('earthquake_components')
          
            messages.error(request, f'Component {delete_componentID} not found!')
            return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html')

def status(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            componentID = request.POST.get("componentID")
            status = request.POST.get("statusValue")
            dateTime = datetime.datetime.now()
            user = User.objects.filter(username = request.user.username).first()

            all_components = Device_Sensor.objects.all()
            all_devices = Device.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 2).count()

            current_status = None
            new_status = None
            current_statusIndex = None
            new_statusIndex = int(status)

            for component in all_components:
                if component.device_sensor_id == componentID:
                    current_statusIndex = component.sensor_status
                    component.sensor_status = status
                    component.last_maintained_datetime = dateTime
                    component.last_maintained_by = user
                    component.save()

                    if current_statusIndex == 0:
                        current_status = "Connected"
                    elif current_statusIndex == 1:
                        current_status = "Under Maintenance"
                    elif current_statusIndex == 2:
                        current_status = "Needs Maintenance"
                    else:
                        current_status = "Inactive"

                    if new_statusIndex == 0:
                        new_status = "Connected"
                    elif new_statusIndex == 1:
                        new_status = "Under Maintenance"
                    elif new_statusIndex == 2:
                        new_status = "Needs Maintenance"
                    else:
                        new_status = "Inactive"

                    add_log = AuditLogs.objects.create(    
                        log_id = "ML0" + str(all_userLogs + 1),
                        activity = "Update Sensor Status",
                        username = request.user,
                        audit_details = str(request.user) + " updated " + componentID + "'s status from " + current_status + " to " + new_status + ".",
                        audit_type = 2
                    )
                    add_log.save()

                    messages.success(request, f'Updated {componentID} status successfully!')
                    if component.sensor_id.sensor_type == 0:
                        return redirect('fire_components')
                    elif component.sensor_id.sensor_type == 1:
                        return redirect('flood_components')
                    else:
                        return redirect('earthquake_components')

            for device in all_devices:
                if device.device_id == componentID:
                    current_statusIndex = device.device_status
                    device.device_status = status
                    device.last_maintained_datetime = dateTime
                    device.last_maintained_by = user
                    device.save()

                    if current_statusIndex == 0:
                        current_status = "Connected"
                    elif current_statusIndex == 1:
                        current_status = "Under Maintenance"
                    elif current_statusIndex == 2:
                        current_status = "Needs Maintenance"
                    else:
                        current_status = "Inactive"

                    if new_statusIndex == 0:
                        new_status = "Connected"
                    elif new_statusIndex == 1:
                        new_status = "Under Maintenance"
                    elif new_statusIndex == 2:
                        new_status = "Needs Maintenance"
                    else:
                        new_status = "Inactive"

                    add_log = AuditLogs.objects.create(    
                        log_id = "ML0" + str(all_userLogs + 1),
                        activity = "Update Device Status",
                        username = request.user,
                        audit_details = str(request.user) + " updated " + componentID + "'s status from " + current_status + " to " + new_status + ".",
                        audit_type = 2
                    )
                    add_log.save()

                    messages.success(request, f'Updated {componentID} status successfully!')
                    return redirect('devices')
          
            messages.error(request, f'Component {componentID} not found!')
            return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html')