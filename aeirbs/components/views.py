from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from reports.models import AuditLogs, IncidentReport, Incident
from django.db.models import Q
from django.template.loader import render_to_string

from django.core.mail import EmailMessage, EmailMultiAlternatives
from aeirbs.helper import format_input, format_portNumber, remove_whitespace, get_floorLocations
from aeirbs.helper import validate_stringFormat, validate_emailFormat, validate_URLFormat, validate_portNumber, validate_voltage
from aeirbs.helper import sort_filter_components

from .models import Alarm, Sensor, Device, Device_Sensor, INCIDENT_TYPE, STATUS, DEFAULT_IMAGE
from accounts.models import JobPosition 
from reports.models import AuditLogs

import serial
import json
import datetime


# Create your views here.
FLOOR_LOCATIONS = get_floorLocations()
# Connect to Arduino
def getArduinoData(comp_port):
    try:
        sr = serial.Serial(comp_port,9600)
        st = list(str(sr.readline(),'utf-8'))
        sr.close() 
        return (str(''.join(st[:])).split())
    except:
        return [0, 0]

def ajax_data(request):
    port = request.POST.get("port")
    ard = getArduinoData(port)
    data = {'distance': float(ard[0]), 'temp': float(ard[1])}
    componentID = request.POST.get("componentID")

    all_components = Device_Sensor.objects.all()
    all_devices = Device.objects.filter(device_status = 0) | Device.objects.filter(device_status = 2)
    all_incidents = Incident.objects.all()
    all_userLogs = AuditLogs.objects.filter(audit_type = 2).count()

    alert = 0
    current_device = None
    current_incident = None

    for device in all_devices:
        if device.id == int(componentID):
            current_device = device
            break
    
    for incident in all_incidents:
        #print(current_device, incident.id)
        #print(current_device, current_device.device_type)
        if incident.id == current_device.device_type:
            current_incident = incident
    
    #print(current_device, current_incident)


    # no arduino present
    if float(ard[0]) == 0.0 and float(ard[1]) == 0.0:
        # check if it's a new disconnection
        if current_device.device_status != 2:
            current_device.device_status = 2
            current_device.save()

            add_mlog = AuditLogs.objects.create(    
                log_id = "ML0" + str(all_userLogs + 1),
                activity = "Disconnected Device",
                is_auto = True,
                audit_details = current_device.device_id + " is disconnected from the system",
                audit_type = 2
            )
            add_mlog.save()

        for component in all_components:
            if component.device_id_id == current_device.id:
                #print("went in EQ0")
                component.connectivity_status = 0
                component.sensor_status = 2
                component.save()

    # arduino is present
    else:
        current_device.device_status = 0
        current_device.save()

        current_devsens = []

        for component in all_components:
            if component.device_id_id == current_device.id:
                #print("went in NEQ0")
                current_devsens.append(component)
                component.connectivity_status = 1
                component.sensor_status = 0
                component.save()

        # check earthquake threshold
        # ard[0] - Triple Axis Accelerometer
        print(current_device.device_type)
        if current_device.device_type == 1:
            # EQ 3
            if float(ard[0]) >= 15.0:
                print('earthquake happening')
                alert = 1

                # print(current_device, current_incident)
                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "EQ_I",
                )
                add_increp.save()

            # EQ 2
            if float(ard[0]) >= 10.0 and 15 > float(ard[0]):
                print('earthquake happening')
                alert = 1

                # print(current_device, current_incident)
                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "EQ_II",
                )
                add_increp.save()


            if float(ard[0]) >= 5.0 and 10 > float(ard[0]):
                print('earthquake happening')
                alert = 1

                # print(current_device, current_incident)
                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "EQ_III",
                )
                add_increp.save()
        
        # check fire threshold
        # ard[0] - MQ2 Gas Sensor
        # ard[1] - Temperature Sensor
        if current_device.device_type == 2:
            print(ard[0])
            print(float(ard[1]) >=10.0)
            # check if a sensor is disconnected
            if float(ard[0]) == 0.0:
                current_devsens[0].connectivity_status = 0
                current_devsens[0].sensor_status = 2

                add_mlog = AuditLogs.objects.create(    
                    log_id = "ML0" + str(all_userLogs + 1),
                    activity = "Disconnected Sensor",
                    is_auto = True,
                    audit_details = current_devsens[0].device_sensor_id + " is disconnected from the system",
                    audit_type = 2
                )
                add_mlog.save()
            elif float(ard[1]) == 0.0:
                current_devsens[1].connectivity_status = 0
                current_devsens[1].sensor_status = 2

                add_mlog = AuditLogs.objects.create(    
                    log_id = "ML0" + str(all_userLogs + 1),
                    activity = "Disconnected Sensor",
                    is_auto = True,
                    audit_details = current_devsens[1].device_sensor_id + " is disconnected from the system",
                    audit_type = 2
                )
                add_mlog.save()
            # used OR because MQ2 Gas Sensor is not available
            # FR_THIRD
            if ((float(ard[0]) >= 400.0) or (float(ard[1]) >= 35.0)) and ((float(ard[0]) < 450.0) or (float(ard[1]) < 40.0)):
                print('fire happening')
                alert = 1

                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "FR_THIRD",
                )
                add_increp.save()
            
            #FR_SECOND
            if ((float(ard[0]) >= 350.0) or (float(ard[1]) >= 30.0)) and ((float(ard[0]) < 400.0) or (float(ard[1]) < 35.0)):
                print('fire happening')
                alert = 1

                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "FR_SECOND",
                )
                add_increp.save()

            #FR_FIRST
            if ((float(ard[0]) >= 300.0) or (float(ard[1]) >= 25.0)) and ((float(ard[0]) < 350.0) or (float(ard[1]) < 30.0)):
                print('fire happening')
                alert = 1

                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "FR_FIRST",
                )
                add_increp.save()

        # check flood threshold
        # ard[0] - Ultrasonic Transducer
        # ard[1] - Water sensor 
        if current_device.device_type == 3:
            # check if a sensor is disconnected
            if float(ard[0]) == 0.0:
                current_devsens[0].connectivity_status = 0
                current_devsens[0].sensor_status = 2

                add_mlog = AuditLogs.objects.create(    
                    log_id = "ML0" + str(all_userLogs + 1),
                    activity = "Disconncted Sensor",
                    is_auto = True,
                    audit_details = current_devsens[0].device_sensor_id + " is disconnected from the system",
                    audit_type = 2
                )
                add_mlog.save()

            elif float(ard[1]) == 0.0:
                current_devsens[1].connectivity_status = 0
                current_devsens[1].sensor_status = 2

                add_mlog = AuditLogs.objects.create(    
                    log_id = "ML0" + str(all_userLogs + 1),
                    activity = "Disconncted Sensor",
                    is_auto = True,
                    audit_details = current_devsens[1].device_sensor_id + " is disconnected from the system",
                    audit_type = 2
                )
                add_mlog.save()

            # used AND because it is a complete module
            # FL_HALFTIRE
            print(float(ard[0]))
            print(5.0 <= float(ard[0]))
            print(float(ard[0]) < 10.0)
            if (5.0 <= float(ard[0]) and float(ard[0]) < 10.0) and float(ard[1]) == 1.0:
                print('flood happening')
                alert = 1
                
                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "FL_HALFTIRE",
                )
                add_increp.save()

            # FL_HALFKNEE
            if (10.0 <= float(ard[0]) and float(ard[0]) < 15.0) and float(ard[1]) == 1.0:
                print('flood happening')
                alert = 1
                
                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "FL_HALFKNEE",
                )
                add_increp.save()

            # FL_GUTTER
            if (15.0 <= float(ard[0]) and float(ard[0]) < 20.0) and float(ard[1]) == 1.0:
                print('flood happening')
                alert = 1
                
                add_increp = IncidentReport.objects.create(
                    device_sensor_id = current_device,
                    incident_type_id = current_incident.id,
                    incident_level = "FL_GUTTER",
                )
                add_increp.save()

    alarms = Alarm.objects.all()

    all_alarms = []

    for alarm in alarms:
        all_alarms.append(alarm.announcement)

    data = {'alert': alert, 'temp': float(ard[1]), 'dist': float(ard[0]), 'floor_locations': FLOOR_LOCATIONS, 'dev_id': current_device.device_id, 'dev_name': current_device.device_name, 'all_alarms': all_alarms}
    return HttpResponse(json.dumps(data))

# auto-email
def autoalarm_mail(request):
    # TEMP - Mail content
    context = {}
    context['deviceID'] = request.POST.get('device_id')
    deviceType = request.POST.get('device_type')
    all_sa = User.objects.filter(is_superuser=1, is_active=1)

    emails = ['aeirbs@gmail.com']

    for sa in all_sa:
        emails.append(sa.email)

    if deviceType == 1:
        context['deviceType'] = "Earthquake"
    elif deviceType == 2:
        context['deviceType'] = "Fire"
    else:
        context['deviceType'] = "Flood"
    
    context['deviceFloor'] = request.POST.get('device_floor')
    print(context)
    mail_body = render_to_string('mail/mail_alarm.html', context = context)
    email = EmailMessage("AEIRBS: EMERGENCY", mail_body, "aeirbs@gmail.com", emails)
    email.content_subtype = 'html'

    send_email = email.send()
    return HttpResponse('%s'%send_email)

def add_component(request):
    if request.user.is_authenticated:
        context = {}
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        return render(request, 'SETTINGS-AddComponent.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def fire_components(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['fire_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted=False).order_by('device_id__device_id')
       
        context['sort'] = 'id'
        context['filter'] = 1
        context['ascending_descending'] = 'asc'
        context['count'] = Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted=False).count()
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        all_components = Device_Sensor.objects.all()
        if request.method == 'POST':
            if request.POST.get('keyword'):
                keyword = request.POST.get('keyword')
                context['fire_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted = False, sensor_id__sensor_name__contains = keyword) | Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted = False, device_sensor_id__contains = keyword)
                context['count'] = (Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted = False, sensor_id__sensor_name__contains = keyword) | Device_Sensor.objects.filter(sensor_id__sensor_type=1, device_sensor_isDeleted = False, device_sensor_id__contains = keyword)).count()

            else:
                sortBy = request.POST.get('sortComponent')
                filterBy = int(request.POST.get('filterComponent'))
                asc_desc = request.POST.get('ascDesc')
                print(sortBy)
                print(filterBy)
                context['fire_components'] = sort_filter_components(request, 1, sortBy, filterBy, asc_desc)
                context['count'] = sort_filter_components(request, 1, sortBy, filterBy, asc_desc).count()
                context['sort'] = sortBy
                context['filter'] = filterBy
                context['ascending_descending'] = asc_desc

        return render(request, 'DASHBOARD-FireComponents.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')
        
def earthquake_components(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['earthquake_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=0, device_sensor_isDeleted = False).order_by('device_id__device_id')
       
        context['sort'] = 'id'
        context['filter'] = 1
        context['ascending_descending'] = 'asc'
        context['count'] = Device_Sensor.objects.filter(sensor_id__sensor_type=0, device_sensor_isDeleted = False).count()
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        all_components = Device_Sensor.objects.all()
        if request.method == 'POST':
            if request.POST.get('keyword'):
                keyword = request.POST.get('keyword')
                context['earthquake_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=0, device_sensor_isDeleted = False, sensor_id__sensor_name__contains = keyword) | Device_Sensor.objects.filter(sensor_id__sensor_type=0, device_sensor_isDeleted = False, device_sensor_id__contains = keyword)
                context['count'] = (Device_Sensor.objects.filter(sensor_id__sensor_type=0, device_sensor_isDeleted = False, sensor_id__sensor_name__contains = keyword) | Device_Sensor.objects.filter(sensor_id__sensor_type=0, device_sensor_isDeleted = False, device_sensor_id__contains = keyword)).count()
            else:
                sortBy = request.POST.get('sortComponent')
                filterBy = int(request.POST.get('filterComponent'))
                asc_desc = request.POST.get('ascDesc')
                print(sortBy)
                print(filterBy)
                context['earthquake_components'] = sort_filter_components(request, 0, sortBy, filterBy, asc_desc)
                context['count'] = sort_filter_components(request, 0, sortBy, filterBy, asc_desc).count()
                context['sort'] = sortBy
                context['filter'] = filterBy
                context['ascending_descending'] = asc_desc
                
        return render(request, 'DASHBOARD-EarthquakeComponents.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def flood_components(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['flood_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=2, device_sensor_isDeleted=False).order_by('device_id__device_id')
       
        context['sort'] = 'id'
        context['filter'] = 1
        context['ascending_descending'] = 'asc'
        context['count'] = Device_Sensor.objects.filter(sensor_id__sensor_type=2, device_sensor_isDeleted=False).count()
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['sensor_reading'] = " "#getArduinoData()

        all_components = Device_Sensor.objects.all()
        if request.method == 'POST':
            if request.POST.get('keyword'):
                keyword = request.POST.get('keyword')
                context['flood_components'] = Device_Sensor.objects.filter(sensor_id__sensor_type=2, device_sensor_isDeleted = False, sensor_id__sensor_name__contains = keyword) | Device_Sensor.objects.filter(sensor_id__sensor_type=2, device_sensor_isDeleted = False, device_sensor_id__contains = keyword)
                context['count'] = (Device_Sensor.objects.filter(sensor_id__sensor_type=2, device_sensor_isDeleted = False, sensor_id__sensor_name__contains = keyword) | Device_Sensor.objects.filter(sensor_id__sensor_type=2, device_sensor_isDeleted = False, device_sensor_id__contains = keyword)).count()
            else:
                sortBy = request.POST.get('sortComponent')
                filterBy = int(request.POST.get('filterComponent'))
                asc_desc = request.POST.get('ascDesc')
                print(sortBy)
                print(filterBy)
                context['flood_components'] = sort_filter_components(request, 2, sortBy, filterBy, asc_desc)
                context['count'] = sort_filter_components(request, 2, sortBy, filterBy, asc_desc).count()
                context['sort'] = sortBy
                context['filter'] = filterBy
                context['ascending_descending'] = asc_desc

        return render(request, 'DASHBOARD-FloodComponents.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def devices(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False).order_by('device_id')
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False)
        context['all_components'] = Device_Sensor.objects.all()

        context['sort'] = 'id'
        context['filter'] = 1
        context['ascending_descending'] = 'asc'
        context['count'] =  Device.objects.filter(device_isDeleted=False).count()
        context['floor_locations'] = get_floorLocations()
        context['incident_type'] = INCIDENT_TYPE
        context['status'] = STATUS

        context['all_alarms'] = Alarm.objects.all()
        context['all_positions'] = JobPosition.objects.filter(position_isDeleted = False)

        context['sensor_reading'] = " "#getArduinoData()

        if request.method == 'POST':
            if request.POST.get('keyword'):
                keyword = request.POST.get('keyword')
                context['all_devices'] = Device.objects.filter(device_isDeleted=False, device_name__contains = keyword) | Device.objects.filter(device_isDeleted = False, device_id__contains = keyword)
                context['count'] = (Device.objects.filter(device_isDeleted=False, device_name__contains = keyword) | Device.objects.filter(device_isDeleted = False, device_id__contains = keyword)).count()
            elif request.POST.get('keyword-jobPosition'):
                keyword = request.POST.get('keyword-jobPosition')
                context['all_positions'] = JobPosition.objects.filter(position_isDeleted = False, job_position__contains = keyword)
            else:
                sortBy = request.POST.get('sortComponent')
                filterBy = int(request.POST.get('filterComponent'))
                asc_desc = request.POST.get('ascDesc')
                context['all_devices'] = sort_filter_components(request, 4, sortBy, filterBy, asc_desc)
                context['count'] = sort_filter_components(request, 4, sortBy, filterBy, asc_desc).count()
                context['sort'] = sortBy
                context['filter'] = filterBy
                context['ascending_descending'] = asc_desc

        return render(request, 'SETTINGS-Devices.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def sensors(request):
    if request.user.is_authenticated:
        context = {}
        context['all_devices'] =  Device.objects.filter(device_isDeleted=False)
        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False).order_by('sensor_id')
        context['all_components'] = Device_Sensor.objects.all()
       
        context['sort'] = 'id'
        context['ascending_descending'] = 'asc'
        context['count'] = Sensor.objects.filter(sensor_isDeleted=False).count()
        context['floor_locations'] = FLOOR_LOCATIONS
        context['incident_type'] = INCIDENT_TYPE

        context['all_alarms'] = Alarm.objects.all()
        context['all_positions'] = JobPosition.objects.filter(position_isDeleted = False)

        context['sensor_reading'] = " "#getArduinoData()

        if request.method == 'POST':
            if request.POST.get('keyword'):
                keyword = request.POST.get('keyword')
                context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False, sensor_name__contains = keyword) | Sensor.objects.filter(sensor_isDeleted = False, sensor_id__contains = keyword)
                context['count'] = (Sensor.objects.filter(sensor_isDeleted=False, sensor_name__contains = keyword) | Sensor.objects.filter(sensor_isDeleted = False, sensor_id__contains = keyword)).count()

            else:
                sortBy = request.POST.get('sortComponent')
                asc_desc = request.POST.get('ascDesc')
                print(sortBy)
                print(asc_desc)
                if asc_desc == 'asc':
                    if sortBy == 'type':
                        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False).order_by('sensor_type')
                    else:
                        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False).order_by('sensor_id')
                else:
                    if sortBy == 'type':
                        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False).order_by('-sensor_type')
                    else:
                        context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False).order_by('-sensor_id')

                context['sort'] = sortBy
                context['ascending_descending'] = asc_desc

        return render(request, 'SETTINGS-Sensors.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def add_device(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            #Get User Input
            add_deviceProductID = request.POST.get("addDeviceProductID")
            add_deviceFloorLocation = request.POST.get("addDeviceFloorLocation")
            add_deviceName = request.POST.get("addDeviceName")
            add_deviceLink = request.POST.get("addDeviceLink")
            add_devicePortNumber = request.POST.get("addDevicePortNumber")
            add_deviceImage = request.FILES.get("addDeviceImage")

            #Validate User Input
            if not add_deviceProductID.strip():
                errors["error_deviceProductIDEmpty"] = "Product ID is required."

            if not add_deviceFloorLocation.strip():
                errors["error_floorLocationEmpty"] = "Floor Location is required."
            
            if not add_deviceName.strip():
                errors["error_deviceNameEmpty"] = "Device Name is required."
            else: 
                if not validate_stringFormat(add_deviceName):
                    errors["error_deviceNameFormat"] = "Invalid, input should only contain letters." 

            if not add_deviceLink.strip():
                errors["error_deviceLinkEmpty"] = "Link to Manual/ Datasheet is required."
            else:
                if not validate_URLFormat(add_deviceLink):
                    errors["error_deviceLinkFormat"] = "Invalid, please input a valid URL."
            
            if not add_devicePortNumber.strip():
                errors["error_portNumberEmpty"] = "Port Number is required."
            else:
                if not validate_portNumber(add_devicePortNumber):
                    errors["error_portNumberFormat"] = "Invalid, please input a valid Port Number."

            context["inputDeviceProductID"] = add_deviceProductID
            context["inputDeviceFloorLocation"] = add_deviceFloorLocation
            context["inputDeviceName"] = add_deviceName
            context["inputDeviceLink"] = add_deviceLink
            context["inputDevicePortNumber"] = add_devicePortNumber
            context["errors"] = errors
            context["addComponent"] = "device"
            context["floor_locations"] = FLOOR_LOCATIONS

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'SETTINGS-AddComponent.html',  context = context)
            else:
                #Format User Input
                add_deviceName = format_input(add_deviceName)
                add_devicePortNumber = format_portNumber(add_devicePortNumber)            
                name = remove_whitespace(add_deviceName)
                name = name[0:5].upper()
                count = (Device.objects.filter(device_name = add_deviceName)).count()
                add_deviceID = "DEV-" + name + "-" + str(count + 1)  
                if add_deviceImage == None:
                    add_deviceImage = DEFAULT_IMAGE
                
                #Add Device
                add_device = Device.objects.create(
                    device_id = add_deviceID,
                    device_productID = add_deviceProductID,
                    device_name = add_deviceName,
                    port_number = add_devicePortNumber,
                    floor_location = add_deviceFloorLocation,
                    device_link = add_deviceLink,
                    device_image = add_deviceImage,
                )
                add_device.save()

                #Create Component Log
                add_log = AuditLogs.objects.create(
                    log_id = "CL0" + str(all_userLogs + 1),
                    activity = "Add Device",
                    username = request.user,
                    audit_details = str(request.user) + " added component " + str(add_deviceID) + " to the system.",
                    audit_type = 0
                )
                add_log.save()

                messages.success(request, f'Added component {add_deviceID} successfully!')
                return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')

def add_sensor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_sensors = Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            #Get User Input
            add_sensorType = request.POST.get("addSensorIncidentType")
            add_sensorData = request.POST.get("addSensorData")
            add_sensorProductID = request.POST.get("addSensorProductID")
            add_sensorVoltage = request.POST.get("addSensorVoltage")
            add_sensorName = request.POST.get("addSensorName")
            add_sensorLink = request.POST.get("addSensorLink")
            add_sensorImage = request.FILES.get("addSensorImage")

            #Validate User Input
            if not add_sensorType.strip():
                errors["error_sensorTypeEmpty"] = "Sensor Type is required."
            else:
                add_sensorType = int(add_sensorType)
            
            if not add_sensorData.strip():
                errors["error_sensorDataEmpty"] = "Sensor Data is required."

            if not add_sensorProductID.strip():
                errors["error_sensorProductIDEmpty"] = "Product ID is required."

            if not add_sensorVoltage.strip():
                errors["error_sensorVoltageEmpty"] = "Sensor Voltage is required."
            else:
                if not validate_voltage(add_sensorVoltage):
                    errors["error_sensorVoltageFormat"] = "Invalid, please input a valid Voltage."
            
            if not add_sensorName.strip():
                errors["error_sensorNameEmpty"] = "Sensor Name is required."
            else:
                if not validate_stringFormat(add_sensorName):
                    errors["error_sensorNameFormat"] = "Invalid, input should only contain letters." 

            if not add_sensorLink.strip():
                errors["error_sensorLinkEmpty"] = "Link to Manual/ Datasheet is required."
            else:
                if not validate_URLFormat(add_sensorLink):
                    errors["error_sensorLinkFormat"] = "Invalid, please input a valid URL."

            context["inputSensorType"] = add_sensorType
            context["inputSensorData"] = add_sensorData
            context["inputSensorProductID"] = add_sensorProductID
            context["inputSensorVoltage"] = add_sensorVoltage
            context["inputSensorName"] = add_sensorName
            context["inputSensorLink"] = add_sensorLink
            context["errors"] = errors
            context["addComponent"] = "sensor"
            context['incident_type'] = INCIDENT_TYPE

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'SETTINGS-AddComponent.html',  context = context)
            else:
                #Format User Input
                add_sensorName = format_input(add_sensorName)

                if add_sensorImage == None:
                    add_sensorImage = DEFAULT_IMAGE
            
                name = remove_whitespace(add_sensorName)
                name= name[0:5].upper()

                if add_sensorType == 0:
                    type = "EQ"
                elif add_sensorType == 1:
                    type = "FR"
                else:
                    type = "FL"

                count = Sensor.objects.filter(sensor_type = add_sensorType).count()

                add_sensorID = type + "SEN-"  + name + "-" + str(count + 1)

                #Add Sensor
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
                    
                    #Create Component Log
                    add_log = AuditLogs.objects.create(
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Add Sensor",
                        username = request.user,
                        audit_details = str(request.user) + " added sensor " + str(add_sensorID) + " to the system.",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Added sensor {add_sensorID} successfully!')      
                return redirect('sensors')    
    else:
        return render(request, 'AEIRBS-Login.html')

def add_comp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            all_devices = Device.objects.all()
            all_sensors = Sensor.objects.all()
            all_components = Device_Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()
            universal = False
            sensor_connected = [] 

            #Get User Input
            add_deviceID = request.POST.get("addDeviceID")
            add_sensorID = request.POST.get("addSensorID")

            #Validate User Input
            for device in all_devices:
                if device.device_id == add_deviceID:
                    if device.device_type == 0:
                        universal = True
                    else:
                        device_type = device.device_type - 1

            for component in all_components:
                if component.device_id.device_id == add_deviceID:
                    sensor_connected.append(component.sensor_id.sensor_name)    

            
            #Format User Input
            deviceID = Device.objects.filter(device_id = add_deviceID).first()
            sensorID = Sensor.objects.filter(sensor_id = add_sensorID).first()

            for sensor in all_sensors:
                if sensor.sensor_id == add_sensorID:
                    name = format_input(sensor.sensor_name)
                    if sensor.sensor_type == 0:
                        sensor_typeIndex = 0
                        sensor_type = "EQ"
                    elif sensor.sensor_type == 1:
                        sensor_typeIndex = 1
                        sensor_type = "FR"
                    else:
                        sensor_typeIndex = 2
                        sensor_type = "FL"
                    break

            for device in all_devices:
                if device.device_id == add_deviceID:
                    floor_location = device.floor_location
                    break

            if not universal:
                if device_type == sensor_typeIndex and name not in sensor_connected:
                    name = remove_whitespace(name)
                    name = name[0:5].upper()
                    count = Device_Sensor.objects.filter(sensor_id__sensor_type__contains = sensor_typeIndex).count()
                    add_device_sensorID = sensor_type + "DS-"  + name + "-" + str(count + 1)

                    #Add Component
                    add_component = Device_Sensor.objects.create(
                        device_sensor_id = add_device_sensorID,
                        device_id = deviceID,
                        sensor_id = sensorID,
                    )
                    add_component.save()

                    device_count = Device_Sensor.objects.filter(device_id__device_id = add_deviceID, device_sensor_isDeleted = False).count()

                    for device in all_devices:
                        if device.device_id == add_deviceID:
                            if device_count >= 2:
                                device.device_maxedOut = True
                            else:
                                device.device_maxedOut = False
                        device.save()

                    #Create Component Log
                    add_log = AuditLogs.objects.create(
                        log_id = "CL0" + str(all_userLogs + 1),
                        activity = "Connect Sensor",
                        username = request.user,
                        audit_details = str(request.user) + " connected sensor " + str(sensorID) + " to " + str(deviceID) + ".",
                        audit_type = 0
                    )
                    add_log.save()

                    messages.success(request, f'Connected sensor {sensorID} to {deviceID} successfully!')
                    for sensor in all_sensors:
                        if sensor.sensor_id == add_sensorID:
                            if sensor.sensor_type == 0:
                                return redirect('earthquake_components')
                            elif sensor.sensor_type == 1:
                                return redirect('fire_components')    
                            else:
                                return redirect('flood_components')
                else:
                    if not device_type == sensor_typeIndex:
                        messages.error(request, f'Error connecting Sensor. Please connect according to Device Type')
                        return redirect('devices')
                    if name in sensor_connected:
                        messages.error(request, f'Error connecting Sensor. Sensor is already connected in this Device.')
                        return redirect('devices')
            else:
                name = remove_whitespace(name)
                name = name[0:5].upper()
                count = Device_Sensor.objects.filter(sensor_id__sensor_type__contains = sensor_typeIndex).count()
                add_device_sensorID = sensor_type + "DS-"  + name + "-" + str(count + 1)
                    
                #Add Component
                add_component = Device_Sensor.objects.create(
                    device_sensor_id = add_device_sensorID,
                    device_id = deviceID,
                    sensor_id = sensorID,
                )
                add_component.save()

                device_count = Device_Sensor.objects.filter(device_id__device_id = add_deviceID, device_sensor_isDeleted = False).count()

                for device in all_devices:
                    if device.device_id == add_deviceID:
                        device.device_type = sensor_typeIndex + 1
                        if device_count >= 2:
                            device.device_maxedOut = True
                        else:
                            device.device_maxedOut = False
                    device.save()

                #Create Component Log
                add_log = AuditLogs.objects.create(
                    log_id = "CL0" + str(all_userLogs + 1),
                    activity = "Connect Sensor",
                    username = request.user,
                    audit_details = str(request.user) + " connected sensor " + str(sensorID) + " to " + str(deviceID) + ".",
                    audit_type = 0
                )
                add_log.save()

                messages.success(request, f'Connected sensor {sensorID} to {deviceID} successfully!')
                for sensor in all_sensors:
                    if sensor.sensor_id == add_sensorID:
                        if sensor.sensor_type == 0:
                            return redirect('earthquake_components')
                        elif sensor.sensor_type == 1:
                            return redirect('fire_components')    
                        else:
                            return redirect('flood_components')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_device(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_devices = Device.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            deviceID = request.POST.get("editDeviceID")
            edit_deviceName = request.POST.get("editDeviceName")
            edit_deviceProductID = request.POST.get("editDeviceProductID")
            edit_devicePortNumber = request.POST.get("editDevicePortNumber")
            edit_deviceFloorLocation = request.POST.get("editDeviceFloorLocation")
            edit_deviceLink = request.POST.get("editDeviceLink")
            edit_deviceImage = request.FILES.get("editDeviceImage")

            #Validate User Input
            if not edit_deviceProductID.strip():
                errors["error_deviceProductIDEmpty"] = "Product ID is required."

            if not edit_deviceFloorLocation.strip():
                errors["error_floorLocationEmpty"] = "Floor Location is required."
            
            if not edit_deviceName.strip():
                errors["error_deviceNameEmpty"] = "Device Name is required."
            else: 
                if not validate_stringFormat(edit_deviceName):
                    errors["error_deviceNameFormat"] = "Invalid, input should only contain letters." 

            if not edit_deviceLink.strip():
                errors["error_deviceLinkEmpty"] = "Link to Manual/ Datasheet is required."
            else:
                if not validate_URLFormat(edit_deviceLink):
                    errors["error_deviceLinkFormat"] = "Invalid, please input a valid URL."
            
            if not edit_devicePortNumber.strip():
                errors["error_portNumberEmpty"] = "Port Number is required."
            else:
                if not validate_portNumber(edit_devicePortNumber):
                    errors["error_portNumberFormat"] = "Invalid, please input a valid Port Number."
                    
            context['error'] = True
            context['deviceID'] = deviceID
            context["inputDeviceProductID"] = edit_deviceProductID
            context["inputDeviceFloorLocation"] = edit_deviceFloorLocation
            context["inputDeviceName"] = edit_deviceName
            context["inputDeviceLink"] = edit_deviceLink
            context["inputDevicePortNumber"] = edit_devicePortNumber
            context["errors"] = errors
            context['all_devices'] =  Device.objects.filter(device_isDeleted=False).order_by('device_id')
            context["floor_locations"] = FLOOR_LOCATIONS

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'SETTINGS-Devices.html',  context = context)
            else:

                for device in all_devices:
                    if device.device_id == deviceID:
                        if edit_deviceImage == None:
                            edit_deviceImage = device.device_image
                        device.device_id = deviceID
                        device.device_name = edit_deviceName
                        device.device_productID = edit_deviceProductID
                        device.mac_address = edit_devicePortNumber
                        device.floor_location = edit_deviceFloorLocation
                        device.device_link = edit_deviceLink
                        device.device_image = edit_deviceImage
                        device.save()

                        add_log = AuditLogs.objects.create(    
                            log_id = "CL0" + str(all_userLogs + 1),
                            activity = "Edit Device",
                            username = request.user,
                            audit_details = str(request.user) + " updated device " + deviceID + "'s details.",
                            audit_type = 0
                        )
                        add_log.save()
                        
                        messages.success(request, f'Updated {deviceID} successfully!')
                        return redirect('devices')
            
                messages.error(request, f'Device {deviceID} not found!')
                return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_sensor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_components = Device_Sensor.objects.all()
            all_sensors = Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            #Get User Input
            sensorID = request.POST.get("editSensorID")
            edit_sensorType = request.POST.get("editSensorIncidentType")
            edit_sensorProductID = request.POST.get("editSensorProductID")
            edit_sensorName = request.POST.get("editSensorName")
            edit_sensorData = request.POST.get("editSensorData")
            edit_sensorVoltage = request.POST.get("editSensorVoltage")
            edit_sensorLink = request.POST.get("editSensorLink")
            edit_sensorImage = request.FILES.get("editSensorImage")

            #Validate User Input
            if not edit_sensorType.strip():
                errors["error_sensorTypeEmpty"] = "Sensor Type is required."
            else:
                edit_sensorType = int(edit_sensorType)
            
            if not edit_sensorData.strip():
                errors["error_sensorDataEmpty"] = "Sensor Data is required."

            if not edit_sensorProductID.strip():
                errors["error_sensorProductIDEmpty"] = "Product ID is required."

            if not edit_sensorVoltage.strip():
                errors["error_sensorVoltageEmpty"] = "Sensor Voltage is required."
            else:
                if not validate_voltage(edit_sensorVoltage):
                    errors["error_sensorVoltageFormat"] = "Invalid, please input a valid Voltage."
            
            if not edit_sensorName.strip():
                errors["error_sensorNameEmpty"] = "Sensor Name is required."
            else:
                if not validate_stringFormat(edit_sensorName):
                    errors["error_sensorNameFormat"] = "Invalid, input should only contain letters." 

            if not edit_sensorLink.strip():
                errors["error_sensorLinkEmpty"] = "Link to Manual/ Datasheet is required."
            else:
                if not validate_URLFormat(edit_sensorLink):
                    errors["error_sensorLinkFormat"] = "Invalid, please input a valid URL."

            context['error'] = True
            context['sensorID'] = sensorID
            context["inputSensorType"] = edit_sensorType
            context["inputSensorData"] = edit_sensorData
            context["inputSensorProductID"] = edit_sensorProductID
            context["inputSensorVoltage"] = edit_sensorVoltage
            context["inputSensorName"] = edit_sensorName
            context["inputSensorLink"] = edit_sensorLink
            context["errors"] = errors
            context['all_sensors'] = Sensor.objects.filter(sensor_isDeleted=False).order_by('sensor_id')
            context['incident_type'] = INCIDENT_TYPE

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'SETTINGS-Sensors.html', context = context)
            else: 
                #Format User Input
                edit_sensorName = format_input(edit_sensorName)

                if edit_sensorType == 0:
                    type = "EQ"
                elif edit_sensorType == 1:
                    type = "FR"
                else:
                    type = "FL"

                #Update Sensor
                for sensor in all_sensors:
                    if sensor.sensor_id == sensorID:
                        if edit_sensorImage == None:
                            edit_sensorImage = sensor.sensor_image
                        sensor.sensor_type = edit_sensorType
                        sensor.sensor_name = edit_sensorName
                        sensor.sensor_productID = edit_sensorProductID
                        sensor.sensor_data = edit_sensorData
                        sensor.sensor_volatage = edit_sensorVoltage 
                        sensor.sensor_link = edit_sensorLink
                        sensor.sensor_image = edit_sensorImage
                        sensor.save()

                        eqcounter = 1
                        frcounter = 1
                        flcounter = 1

                        #Update All Components
                        for component in all_components:
                            name = remove_whitespace(component.sensor_id.sensor_name)
                            name = name[0:5].upper()
                            if component.sensor_id.sensor_type == 0:
                                id = "EQDS-" + name + "-" + str(eqcounter)
                                eqcounter += 1
                            elif component.sensor_id.sensor_type == 1:
                                id = "FRDS-" + name + "-" + str(frcounter) 
                                frcounter += 1
                            else:
                                id = "FLDS-" + name + "-" + str(flcounter)
                                flcounter += 1

                            component.device_sensor_id = id
                            component.save()
                            continue

                        eqcounter = 1
                        frcounter = 1
                        flcounter = 1
                        
                        #Update All Sensors
                        for sensor in all_sensors:
                            name = remove_whitespace(sensor.sensor_name)
                            name = name[0:5].upper()
                            if sensor.sensor_type == 0:
                                id = "EQSEN-" + name + "-" + str(eqcounter)
                                eqcounter += 1
                            elif sensor.sensor_type == 1:
                                id = "FRSEN-" + name + "-" + str(frcounter)
                                frcounter += 1
                            else:
                                id = "FLSEN-" + name + "-" + str(flcounter)
                                    
                            sensor.sensor_id = id
                            sensor.save()
                            continue
                        
                        #Create Component Logs
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
            all_components = Device_Sensor.objects.all()
            all_devices = Device.objects.all()
            all_sensors = Sensor.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()
            universal = False
            sensor_connected = [] 

            componentID = request.POST.get("editComponentID")
            deviceID = request.POST.get("editComponentDeviceID")

            #Validate User Input
            for device in all_devices:
                if device.device_id == deviceID:
                    if device.device_type == 0:
                        universal = True
                    else:
                        device_type = device.device_type - 1

            for component in all_components:
                if component.device_sensor_id == componentID:
                    sensorID = component.sensor_id.sensor_id
                if component.device_id.device_id == deviceID:
                    sensor_connected.append(component.sensor_id.sensor_name)    

            #Format User Input
            edit_deviceID = Device.objects.filter(device_id = deviceID).first()

            for sensor in all_sensors:
                if sensor.sensor_id == sensorID:
                    name = format_input(sensor.sensor_name)
                    if sensor.sensor_type == 0:
                        sensor_typeIndex = 0
                        sensor_type = "EQ"
                    elif sensor.sensor_type == 1:
                        sensor_typeIndex = 1
                        sensor_type = "FR"
                    else:
                        sensor_typeIndex = 2
                        sensor_type = "FL"
                    break

            if not universal:
                if device_type == sensor_typeIndex and name not in sensor_connected:
                    for component in all_components:
                        if component.device_sensor_id == componentID:
                            old_device = component.device_id.device_id
                            component.device_id = edit_deviceID
                            component.save()

                            old_deviceCount = Device_Sensor.objects.filter(device_id__device_id = old_device, device_sensor_isDeleted = False).count()
                            new_deviceCount = Device_Sensor.objects.filter(device_id__device_id = edit_deviceID, device_sensor_isDeleted = False).count()

                            for device in all_devices:
                                if device.device_id == old_device:
                                    if old_deviceCount >= 2:
                                        device.device_maxedOut = True
                                    else:
                                        device.device_maxedOut = False
                                        if old_deviceCount == 0:
                                            device.device_type = 0
                                device.save()

                            for device in all_devices:
                                if device.device_id == edit_deviceID:
                                    if new_deviceCount >= 2:
                                        device.device_maxedOut = True
                                    else:
                                        device.device_maxedOut = False
                                device.save()

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
                                return redirect('earthquake_components')
                            elif component.sensor_id.sensor_type == 1:
                                return redirect('fire_components')
                            else:
                                return redirect('flood_components')
                else:
                    if not device_type == sensor_typeIndex:
                        messages.error(request, f'Error connecting Sensor. Please connect according to Device Type')
                        return redirect('devices')
                    if name in sensor_connected:
                        for component in all_components:
                            if component.device_sensor_id == componentID:
                                old_device = component.device_id.device_id

                                if old_device == deviceID:
                                    messages.error(request, f'Sensor is already connected in this Device.')
                                    return redirect('devices')
                                else:
                                    messages.error(request, f'Error connecting Sensor. Sensor is already connected in this Device.')
                                    return redirect('devices')
            
            else:
                 for component in all_components:
                    if component.device_sensor_id == componentID:
                        old_device = component.device_id.device_id
                        component.device_id = edit_deviceID
                        component.save()

                        old_deviceCount = Device_Sensor.objects.filter(device_id__device_id = old_device, device_sensor_isDeleted = False).count()
                        new_deviceCount = Device_Sensor.objects.filter(device_id__device_id = edit_deviceID, device_sensor_isDeleted = False).count()
                        
                        for device in all_devices:
                            if device.device_id == old_device:
                                if old_deviceCount >= 2:
                                    device.device_maxedOut = True
                                else:
                                    device.device_maxedOut = False
                                    if old_deviceCount == 0:
                                        device.device_type = 0
                            device.save()

                        for device in all_devices: 
                            if device.device_id == deviceID:
                                print("CHANGE SENSOR TYPE")
                                device.device_type = sensor_typeIndex + 1
                                if new_deviceCount >= 2:
                                    device.device_maxedOut = True
                                else:   
                                    device.device_maxedOut = False
                            device.save()

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
                            return redirect('earthquake_components')
                        elif component.sensor_id.sensor_type == 1:
                            return redirect('fire_components')
                        else:
                            return redirect('flood_components')
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
            all_devices = Device.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 0).count()

            for component in all_components:
                if component.device_sensor_id == delete_componentID:
                    deviceID = component.device_id.device_id
                    component.device_sensor_isDeleted = True
                    component.save()

                    device_count = Device_Sensor.objects.filter(device_id__device_id = deviceID, device_sensor_isDeleted = False).count()
                    print(device_count)

                    for device in all_devices:
                        if device.device_id == deviceID:
                            if device_count >= 2:
                                device.device_maxedOut = True
                            else:
                                device.device_maxedOut = False
                                if device_count == 0:
                                    device.device_type = 0
                        device.save()

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
                        return redirect('earthquake_components')
                    elif component.sensor_id.sensor_type == 1:
                        return redirect('fire_components')
                    else:
                        return redirect('flood_components')
          
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
            date_time = dateTime.strftime("%x %X")
            user = User.objects.filter(username = request.user.username).first()

            print(status)

            all_components = Device_Sensor.objects.all()
            all_devices = Device.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 2).count()

            current_status = None
            new_status = None
            current_statusIndex = None
            new_statusIndex = int(status)

            for component in all_components:
                if component.device_sensor_id == componentID:
                    incident_type = component.sensor_id.sensor_type
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
                        return redirect('earthquake_components')
                    elif component.sensor_id.sensor_type == 1:
                        return redirect('fire_components')
                    else:
                        return redirect('flood_components')

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

