
from components.models import Device, Sensor, Device_Sensor, Floor

import string
import validators
import phonenumbers

def format_input(input):
    input_list = input.split()
    format_list = []
    
    for item in input_list:
        item = item[0].upper() + item[1:].lower()
        format_list.append(item)
    
    input =  " ".join(format_list)
    
    return input

def format_portNumber(input):
    if len(input) == 12:
        input = input[0:-4].lower() + input[-4:].upper()
    else:
        input = input[0:3].upper() + input[3:]
    
    return input

def remove_whitespace(input):
    input = input.replace(" ", "")
    return input

def with_letter(input):
    withLetter = False
    
    for char in input:
        if char in string.ascii_letters:
            withLetter = True
            break
    return withLetter

def validate_specialCharacter(input):
    isSpecial = False
    
    for char in input:
        if char in string.punctuation:
            isSpecial = True
                
    return isSpecial
                
def validate_stringFormat(input):
    isValid = True

    for char in input:
        if char not in string.ascii_letters and char not in string.whitespace:
            isValid = False
    
    return isValid

def validate_numberFormat(input):
    isValid = True

    for char in input:
        if char not in string.digits:
            isValid = False

    return isValid

def validate_alphaNumeric(input):
    isValid = True
    
    for char in input:
        if char not in string.digits and char not in string.ascii_letters:
            isValid = False
    
    return isValid

def validate_windowsPortNumber(input):
    isValid = False
    
    input = input.lower()
    if input[0:3] == "com":
        if validate_numberFormat(input[3:]):
            if int(input[3:])> 0 and int(input[3:]) <= 256:
                isValid = True
    
    return isValid

def validate_raspbianPortNumber(input):
    isValid = False
        
    input = input.lower()
    if len(input) == 12:
        if input[0:-1] == "/dev/ttyacm":
            if input[-1] in string.digits:
                if int(input[-1]) >=0 and int(input[-1]) <=3:
                    isValid = True
    
    return isValid

def validate_portNumber(input):
    return(validate_windowsPortNumber(input) or validate_raspbianPortNumber(input))
    

def validate_voltage(input):
    isValid = True
    decimal_count = 0
    
    for char in input:
        if char == '.':
            decimal_count += 1
    print(decimal_count)
    if decimal_count == 1 or decimal_count == 0:
        for char in input:
            if char not in string.digits and char != '.':
                isValid = False
    else:
        isValid = False
        
    return isValid

def validate_URLFormat(input):
    isValid = True
    
    if not validators.url(input):
        isValid = False
        
    return isValid

def validate_emailFormat(input):
    isValid = True
    
    if not validators.email(input):
        isValid = False
        
    return isValid

def validate_mobileNumber(input):
    mobile_number = phonenumbers.parse(input, "PH")    
    return phonenumbers.is_valid_number(mobile_number)

def get_floorLocations():
    floor_locations = []
    floors = Floor.objects.all()

    for floor in floors:
        temp = (floor.floor_identifier, floor.floor_description)
        floor_locations.append(temp)

    return floor_locations 

def sort_filter_components(request, incident_type, sort_by, filter_by, asc_desc):
    if asc_desc == 'asc':
        if incident_type < 4:
            if sort_by == 'floor':
                if filter_by == 2:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_id__floor_location')
                elif filter_by == 3:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__floor_location')
                elif filter_by == 4:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__floor_location')
                elif filter_by == 5:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__floor_location')
                elif filter_by == 6:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1)).order_by('device_id__floor_location')
                elif filter_by == 7:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_id__floor_location')
                elif filter_by == 8:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__floor_location')
                elif filter_by == 9:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_id__floor_location')
                elif filter_by == 10:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__floor_location')
                elif filter_by == 11:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__floor_location')
                elif filter_by == 12:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0).order_by('device_id__floor_location')
                elif filter_by == 13:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1).order_by('device_id__floor_location')
                elif filter_by == 14:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2).order_by('device_id__floor_location')
                elif filter_by == 15:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3).order_by('device_id__floor_location')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device_Sensor.objects.filter(~Q(sensor_status = 1)) & Device_Sensor.objects.filter(~Q(sensor_status = 2)) & Device_Sensor.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False).order_by('device_id__floor_location')

            elif sort_by == 'device':
                if filter_by == 2:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_id__device_id')
                elif filter_by == 3:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__device_id')
                elif filter_by == 4:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__device_id')
                elif filter_by == 5:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__device_id')
                elif filter_by == 6:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1)).order_by('device_id__device_id')
                elif filter_by == 7:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_id__device_id')
                elif filter_by == 8:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__device_id')
                elif filter_by == 9:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_id__device_id')
                elif filter_by == 10:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__device_id')
                elif filter_by == 11:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_id__device_id')
                elif filter_by == 12:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0).order_by('device_id__device_id')
                elif filter_by == 13:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1).order_by('device_id__device_id')
                elif filter_by == 14:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2).order_by('device_id__device_id')
                elif filter_by == 15:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3).order_by('device_id__device_id__device_id__device_id')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device_Sensor.objects.filter(~Q(sensor_status = 1)) & Device_Sensor.objects.filter(~Q(sensor_status = 2)) & Device_Sensor.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False).order_by('device_id__device_id')

            elif sort_by == 'id':
                if filter_by == 2:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_sensor_id')
                elif filter_by == 3:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_sensor_id')
                elif filter_by == 4:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_sensor_id')
                elif filter_by == 5:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_sensor_id')
                elif filter_by == 6:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1)).order_by('device_sensor_id')
                elif filter_by == 7:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_sensor_id')
                elif filter_by == 8:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_sensor_id')
                elif filter_by == 9:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('device_sensor_id')
                elif filter_by == 10:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_sensor_id')
                elif filter_by == 11:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('device_sensor_id')
                elif filter_by == 12:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0).order_by('device_sensor_id')
                elif filter_by == 13:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1).order_by('device_sensor_id')
                elif filter_by == 14:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2).order_by('device_sensor_id')
                elif filter_by == 15:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3).order_by('device_sensor_id')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device_Sensor.objects.filter(~Q(sensor_status = 1)) & Device_Sensor.objects.filter(~Q(sensor_status = 2)) & Device_Sensor.objects.filter(~Q(sensor_status = 3)).order_by('device_sensor_id')
                else:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False).order_by('device_sensor_id')
        else:
            if sort_by == 'floor':
                if filter_by == 2:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('floor_location')
                elif filter_by == 3:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('floor_location')
                elif filter_by == 4:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('floor_location')
                elif filter_by == 5:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('floor_location')
                elif filter_by == 6:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1)).order_by('floor_location')
                elif filter_by == 7:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('floor_location')
                elif filter_by == 8:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('floor_location')
                elif filter_by == 9:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('floor_location')
                elif filter_by == 10:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('floor_location')
                elif filter_by == 11:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('floor_location')
                elif filter_by == 12:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 0).order_by('floor_location')
                elif filter_by == 13:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 1).order_by('floor_location')
                elif filter_by == 14:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 2).order_by('floor_location')
                elif filter_by == 15:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 3).order_by('floor_location')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device.objects.filter(~Q(sensor_status = 1)) & Device.objects.filter(~Q(sensor_status = 2)) & Device.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False).order_by('floor_location')

            elif sort_by == 'id':
                if filter_by == 2:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('device_id')
                elif filter_by == 3:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('device_id')
                elif filter_by == 4:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('device_id')
                elif filter_by == 5:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('device_id')
                elif filter_by == 6:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1)).order_by('device_id')
                elif filter_by == 7:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('device_id')
                elif filter_by == 8:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('device_id')
                elif filter_by == 9:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('device_id')
                elif filter_by == 10:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('device_id')
                elif filter_by == 11:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('device_id')
                elif filter_by == 12:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 0).order_by('device_id')
                elif filter_by == 13:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 1).order_by('device_id')
                elif filter_by == 14:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 2).order_by('device_id')
                elif filter_by == 15:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 3).order_by('device_id')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device.objects.filter(~Q(sensor_status = 1)) & Device.objects.filter(~Q(sensor_status = 2)) & Device.objects.filter(~Q(sensor_status = 3)).order_by('device_id')
                else:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False).order_by('device_id')

    else:
        if incident_type < 4: 
            if sort_by == 'floor':
                if filter_by == 2:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_id__floor_location')
                elif filter_by == 3:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__floor_location')
                elif filter_by == 4:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__floor_location')
                elif filter_by == 5:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__floor_location')
                elif filter_by == 6:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1)).order_by('-device_id__floor_location')
                elif filter_by == 7:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_id__floor_location')
                elif filter_by == 8:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__floor_location')
                elif filter_by == 9:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_id__floor_location')
                elif filter_by == 10:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__floor_location')
                elif filter_by == 11:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__floor_location')
                elif filter_by == 12:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0).order_by('-device_id__floor_location')
                elif filter_by == 13:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1).order_by('-device_id__floor_location')
                elif filter_by == 14:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2).order_by('-device_id__floor_location')
                elif filter_by == 15:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3).order_by('-device_id__floor_location')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device_Sensor.objects.filter(~Q(sensor_status = 1)) & Device_Sensor.objects.filter(~Q(sensor_status = 2)) & Device_Sensor.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False).order_by('-device_id__floor_location')

            elif sort_by == 'device':
                if filter_by == 2:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_id__device_id')
                elif filter_by == 3:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__device_id')
                elif filter_by == 4:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__device_id')
                elif filter_by == 5:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__device_id')
                elif filter_by == 6:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1)).order_by('-device_id__device_id')
                elif filter_by == 7:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_id__device_id')
                elif filter_by == 8:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__device_id')
                elif filter_by == 9:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_id__device_id')
                elif filter_by == 10:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__device_id')
                elif filter_by == 11:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_id__device_id')
                elif filter_by == 12:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0).order_by('-device_id__device_id')
                elif filter_by == 13:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1).order_by('-device_id__device_id')
                elif filter_by == 14:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2).order_by('-device_id__device_id')
                elif filter_by == 15:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3).order_by('-device_id__device_id')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device_Sensor.objects.filter(~Q(sensor_status = 1)) & Device_Sensor.objects.filter(~Q(sensor_status = 2)) & Device_Sensor.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False).order_by('-device_id__device_id')

            elif sort_by == 'id':
                if filter_by == 2:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_sensor_id')
                elif filter_by == 3:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_sensor_id')
                elif filter_by == 4:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_sensor_id')
                elif filter_by == 5:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_sensor_id')
                elif filter_by == 6:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1)).order_by('-device_sensor_id')
                elif filter_by == 7:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_sensor_id')
                elif filter_by == 8:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_sensor_id')
                elif filter_by == 9:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2)).order_by('-device_sensor_id')
                elif filter_by == 10:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_sensor_id')
                elif filter_by == 11:
                    sort_filter_components = (Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2) | Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3)).order_by('-device_sensor_id')
                elif filter_by == 12:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 0).order_by('-device_sensor_id')
                elif filter_by == 13:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 1).order_by('-device_sensor_id')
                elif filter_by == 14:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 2).order_by('-device_sensor_id')
                elif filter_by == 15:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False, sensor_status = 3).order_by('-device_sensor_id')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device_Sensor.objects.filter(~Q(sensor_status = 1)) & Device_Sensor.objects.filter(~Q(sensor_status = 2)) & Device_Sensor.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device_Sensor.objects.filter(sensor_id__sensor_type = incident_type, device_sensor_isDeleted = False).order_by('-device_sensor_id')
        else:
            if sort_by == 'floor':
                if filter_by == 2:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('-floor_location')
                elif filter_by == 3:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-floor_location')
                elif filter_by == 4:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-floor_location')
                elif filter_by == 5:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-floor_location')
                elif filter_by == 6:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1)).order_by('-floor_location')
                elif filter_by == 7:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('-floor_location')
                elif filter_by == 8:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-floor_location')
                elif filter_by == 9:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('-floor_location')
                elif filter_by == 10:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-floor_location')
                elif filter_by == 11:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-floor_location')
                elif filter_by == 12:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 0).order_by('-floor_location')
                elif filter_by == 13:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 1).order_by('-floor_location')
                elif filter_by == 14:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 2).order_by('-floor_location')
                elif filter_by == 15:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 3).order_by('-floor_location')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device.objects.filter(~Q(sensor_status = 1)) & Device.objects.filter(~Q(sensor_status = 2)) & Device.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False).order_by('-floor_location')

            elif sort_by == 'id':
                if filter_by == 2:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('-device_id')
                elif filter_by == 3:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-device_id')
                elif filter_by == 4:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-device_id')
                elif filter_by == 5:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-device_id')
                elif filter_by == 6:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 1)).order_by('-device_id')
                elif filter_by == 7:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('-device_id')
                elif filter_by == 8:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 0) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-device_id')
                elif filter_by == 9:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 2)).order_by('-device_id')
                elif filter_by == 10:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 1) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-device_id')
                elif filter_by == 11:
                    sort_filter_components = (Device.objects.filter(device_isDeleted = False, device_status = 2) | Device.objects.filter(device_isDeleted = False, device_status = 3)).order_by('-device_id')
                elif filter_by == 12:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 0).order_by('-device_id')
                elif filter_by == 13:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 1).order_by('-device_id')
                elif filter_by == 14:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 2).order_by('-device_id')
                elif filter_by == 15:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False, device_status = 3).order_by('-device_id')
                elif filter_by == 16:
                    sort_filter_components = Device_Sensor.objects.filter(~Q(sensor_status = 0)) & Device.objects.filter(~Q(sensor_status = 1)) & Device.objects.filter(~Q(sensor_status = 2)) & Device.objects.filter(~Q(sensor_status = 3))
                else:
                    sort_filter_components = Device.objects.filter(device_isDeleted = False).order_by('-device_id')

    return sort_filter_components