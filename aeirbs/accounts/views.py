from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from reports.models import AuditLogs
from components.models import Device
from .models import JobPosition, Profile, DEFAULT_IMAGE
from django.core.files.storage import FileSystemStorage
import django.contrib.auth.hashers

from django.core.mail import EmailMessage
from datetime import date

from aeirbs.helper import format_input, with_letter, validate_stringFormat, validate_numberFormat, validate_emailFormat, validate_mobileNumber

# auto-email
def addadmin_mail(recipient, lastname, username):
    # TEMP - Mail content
    mail_body = "<div style='margin: 0px 30px 0px;'>" + "<h1>American bobtail tom burmese</h1>" + "<p>Grimalkin tom. Turkish angora grimalkin kitty, or balinese , grimalkin american bobtail but ocicat. Scottish fold grimalkin or himalayan siberian. Egyptian mau scottish fold ocelot, tomcat lion and balinese bombay. Lynx malkin</p><br>" + "<p>Default Password is: " + lastname + username + "</p><br>" + "</div>"

    email = EmailMessage("AEIRBS: Admin Details", mail_body, "damim526@gmail.com", [recipient])
    email.content_subtype = 'html'

    send_email = email.send()

def deladmin_mail(recipient):
    # TEMP - Mail content
    now = date.today().strftime("%d/%m/%Y")

    mail_body = "<div style='margin: 0px 30px 0px;'>" + "<h1>American bobtail tom burmese</h1>" + "<p>Grimalkin tom. Turkish angora grimalkin kitty, or balinese , grimalkin american bobtail but ocicat. Scottish fold grimalkin or himalayan siberian. Egyptian mau scottish fold ocelot, tomcat lion and balinese bombay. Lynx malkin</p><br>" + "<p>YOUR ACCOUNT HAS BEEN TERMINATED AS OF "+ now +"</p><br>" + "</div>"

    email = EmailMessage("AEIRBS: Account termination", mail_body, "damim526@gmail.com", [recipient])
    email.content_subtype = 'html'

    send_email = email.send()

# first login - change password
def login_changepass(request):
    user_newPass = request.POST.get("new_pass")
    print(user_newPass)
    employeeID = request.POST.get("username")
    print(employeeID)
    all_users = User.objects.all()
    all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

    for user in all_users:
        if user.username == employeeID:
            user.set_password(user_newPass)
            user.profile.logged = True
            user.save()

            add_log = AuditLogs.objects.create(
                log_id = "UL0" + str(all_userLogs + 1),
                activity = "Update password",
                username = user,
                audit_details = str(user) + " updated user password from default password.",
                audit_type = 1
            )
            add_log.save()

            messages.success(request, f'Updated user {employeeID} successfully!')
            return redirect('earthquake_components')

    return render(request, 'AEIRBS-Login.html')

# login 
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("company_id")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            # check if user is a new user
            if user.profile.logged == 0:
                return render(request, 'AEIRBS-Login.html', {'new': 1, 'username': username})

            login(request, user)

                # added comment

                # Log: Logged In - Valid User
                all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
                add_log = AuditLogs.objects.create(
                    log_id = "UL0" + str(all_userLogs + 1),
                    activity = "Login",
                    username = request.user,
                    audit_details = str(request.user) + " logged in to the system.",
                    audit_type = 1
                )
                add_log.save()

            messages.success(request, f'Logged in successfully!')
            return redirect('earthquake_components')
        else:
            messages.error(request, f'Invalid credentials.')
            return redirect('login_page')

def logout_action(request):
    # Log: Logged Out

    all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
    add_log = AuditLogs.objects.create(
        log_id = "UL0" + str(all_userLogs + 1),
        activity = "Logout",
        username = request.user,
        audit_details = str(request.user) + " logged out of the system.",
        audit_type = 1
    )
    add_log.save()

    logout(request)
    return redirect('login_page')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html', {'new': 0})

def masterlist(request):
    context = {}
    context['all_users'] = User.objects.all().filter(profile__is_deleted=False)
    context['all_logs'] = AuditLogs.objects.filter(audit_isDeleted=False).order_by('-date_time')
    context['all_devices'] = Device.objects.all()

    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        context['all_users'] = User.objects.filter(profile__is_deleted=False, username__contains = keyword) | User.objects.filter(profile__is_deleted=False, first_name__contains = keyword) | User.objects.filter(profile__is_deleted=False, profile__middle_name__contains = keyword) | User.objects.filter(profile__is_deleted=False, last_name__contains = keyword)
    
    return render(request, 'AEIRBS-Masterlist.html', context = context)

def add_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_users = User.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

            #Get User Input
            add_accessRole = request.POST.get("addAdminAccessRole")
            add_employeeID = request.POST.get("addAdminEmployeeID")
            add_firstName = request.POST.get("addAdminFirstName")
            add_middleName = request.POST.get("addAdminMiddleName")
            add_lastName = request.POST.get("addAdminLastName")
            add_jobPosition = request.POST.get("addAdminJobPosition")
            add_companyEmail = request.POST.get("addAdminCompanyEmail")
            add_mobileNumber = request.POST.get("addAdminMobileNumber")
            add_userImage = request.FILES.get("addAdminImage")

            print(add_accessRole)
            print(add_jobPosition)
            #Validate User Input
            if not add_accessRole.strip():
                errors["error_accessRoleEmpty"] = "Access Role is required."

            if not add_employeeID.strip():
                errors["error_employeeIDEmpty"] = "Employee ID is required."
            
            if not add_firstName.strip():
                errors["error_firstNameEmpty"] = "First Name is required."
            else:
                if not validate_stringFormat(add_firstName):
                    errors["error_firstNameFormat"] = "Invalid, input should only contain letters."

            if not validate_stringFormat(add_middleName):
                errors["error_middleNameFormat"] = "Invalid, input should only contain letters."

            if not add_lastName.strip():
                errors["error_lastNameEmpty"] = "Last Name is required."
            else:
                if not validate_stringFormat(add_lastName):
                    errors["error_lastNameFormat"] = "Invalid, input should only contain letters."

            if not add_jobPosition.strip():
                errors["error_jobPositionEmpty"] = "Job Position is required."
            else:
                if not validate_stringFormat(add_jobPosition):
                    errors["error_jobPositionFormat"] = "Invalid, input should only contain letters."

            if not add_companyEmail.strip():
                errors["error_companyEmailEmpty"] = "Company Email is required."
            else:
                if not validate_emailFormat(add_companyEmail):
                    errors["error_companyEmailFormat"] = "Invalid, please input a valid Email Address."
            
            if not add_mobileNumber.strip():
                errors["error_mobileNumberEmpty"] = "Mobile Number is required."
            else: 
                if with_letter(add_mobileNumber):
                    errors["error_mobileNumberFormat"] = "Invalid, please input a valid Mobile Number."
                else:
                    if not validate_mobileNumber(add_mobileNumber):
                        errors["error_mobileNumberFormat"] = "Invalid, please input a valid Mobile Number."

            if add_accessRole == "adminRole":
                is_super = False
            elif add_accessRole == "superRole":
                is_super = True
            else:
                is_super = None

            context["inputAccessRole"] = is_super
            context["inputEmployeeID"] = add_employeeID
            context["inputFirstName"] = add_firstName
            context["inputMiddleName"] = add_middleName
            context["inputLastName"] = add_lastName
            context["inputJobPosition"] = add_jobPosition
            context["inputMobileNumber"] = add_mobileNumber
            context["inputCompanyEmail"] = add_companyEmail
            context["errors"] = errors
            context["job_positions"] = JobPosition.objects.all()

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'MASTERLIST-AddAdmin.html',  context = context)
            else:
                #Format User Input
                add_firstName = format_input(add_firstName)
                add_middleName = format_input(add_middleName)
                add_lastName = format_input(add_lastName)
                add_jobPosition = format_input(add_jobPosition)
                add_password = add_lastName + add_employeeID
                if add_userImage == None:
                    add_userImage = DEFAULT_IMAGE

                isExisting = False
                for user in all_users:
                    if user.username == add_employeeID:
                        isExisting = True
                
                if isExisting:
                    messages.error(request, f'{add_employeeID} is already registered in the system!')  
                    return render(request, 'MASTERLIST-AddAdmin.html', context = context)
                else:
                    #Add User
                    add_admin = User.objects.create_user(
                        username = add_employeeID,
                        password= add_password,
                        email = add_companyEmail,
                        first_name = add_firstName,
                        last_name = add_lastName,
                        is_superuser = is_super,
                        is_staff = is_super,
                    )
                    add_admin.save()
                    add_admin.refresh_from_db()
                    add_admin.profile.user_image = add_userImage
                    add_admin.profile.middle_name = add_middleName
                    add_admin.profile.job_position = add_jobPosition
                    add_admin.profile.mobile_number = add_mobileNumber
                    add_admin.save()

                    #Generate Confirmation Email
                    addadmin_mail(add_admin.email, add_admin.last_name, add_admin.username)

                    #Create User Log
                    add_log = AuditLogs.objects.create(
                        log_id = "UL0" + str(all_userLogs + 1),
                        activity = "Add User",
                        username = request.user,
                        audit_details = str(request.user) + " added " + add_employeeID + " to the system.",
                        audit_type = 1
                    )
                    add_log.save()

                    messages.success(request, f'Added user {add_employeeID} successfully!')
                    return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_users = User.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

            #Get User Input
            employeeID = request.POST.get("username")
            edit_accessRole = request.POST.get("editAdminAccessRole")
            edit_employeeID = request.POST.get("editAdminEmployeeID")
            edit_firstName = request.POST.get("editAdminFirstName")
            edit_middleName = request.POST.get("editAdminMiddleName")
            edit_lastName = request.POST.get("editAdminLastName")
            edit_jobPosition = request.POST.get("editAdminJobPosition")
            edit_companyEmail = request.POST.get("editAdminCompanyEmail")
            edit_mobileNumber = request.POST.get("editAdminMobileNumber")
            edit_userImage = request.FILES.get("editAdminImage")

            #Validate User Input
            if not edit_accessRole.strip():
                errors["error_accessRoleEmpty"] = "Access Role is required."

            if not edit_employeeID.strip():
                errors["error_employeeIDEmpty"] = "Employee ID is required."
            
            if not edit_firstName.strip():
                errors["error_firstNameEmpty"] = "First Name is required."
            else:
                if not validate_stringFormat(edit_firstName):
                    errors["error_firstNameFormat"] = "Invalid, input should only contain letters."

            if not validate_stringFormat(edit_middleName):
                errors["error_middleNameFormat"] = "Invalid, input should only contain letters."

            if not edit_lastName.strip():
                errors["error_lastNameEmpty"] = "Last Name is required."
            else:
                if not validate_stringFormat(edit_lastName):
                    errors["error_lastNameFormat"] = "Invalid, input should only contain letters."

            if not edit_jobPosition.strip():
                errors["error_jobPositionEmpty"] = "Job Position is required."
            else:
                if not validate_stringFormat(edit_jobPosition):
                    errors["error_jobPositionFormat"] = "Invalid, input should only contain letters."

            if not edit_companyEmail.strip():
                errors["error_companyEmailEmpty"] = "Company Email is required."
            else:
                if not validate_emailFormat(edit_companyEmail):
                    errors["error_companyEmailFormat"] = "Invalid, please input a valid Email Address."
            
            if not edit_mobileNumber.strip():
                errors["error_mobileNumberEmpty"] = "Mobile Number is required."
            else: 
                if with_letter(edit_mobileNumber):
                    errors["error_mobileNumberFormat"] = "Invalid, please input a valid Mobile Number."
                else:
                    if not validate_mobileNumber(edit_mobileNumber):
                        errors["error_mobileNumberFormat"] = "Invalid, please input a valid Mobile Number."

            if edit_accessRole == "adminRole":
                is_super = False
            elif edit_accessRole == "superRole":
                is_super = True
            else:
                is_super = None

            context["username"] = employeeID
            context['all_users'] = all_users
            context['error'] = True
            context["inputAccessRole"] = is_super
            context["inputEmployeeID"] = edit_employeeID
            context["inputFirstName"] = edit_firstName
            context["inputMiddleName"] = edit_middleName
            context["inputLastName"] = edit_lastName
            context["inputJobPosition"] = edit_jobPosition
            context["inputMobileNumber"] = edit_mobileNumber
            context["inputCompanyEmail"] = edit_companyEmail
            context["errors"] = errors

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'MASTERLIST-EditAdmin.html',  context = context)
            else:
                #Format User Input
                edit_firstName = format_input(edit_firstName)
                edit_middleName = format_input(edit_middleName)
                edit_lastName = format_input(edit_lastName)
                edit_jobPosition = format_input(edit_jobPosition)

                #Update User
                for user in all_users:
                    if user.username == employeeID:
                        if edit_userImage == None:
                            edit_userImage = user.profile.user_image
                        user.username = edit_employeeID
                        user.first_name = edit_firstName
                        user.profile.middle_name = edit_middleName
                        user.last_name = edit_lastName
                        user.email = edit_companyEmail
                        user.profile.job_position = edit_jobPosition
                        user.profile.mobile_number = edit_mobileNumber
                        user.profile.user_image = edit_userImage
                        user.save()

                        #Create User Log
                        add_log = AuditLogs.objects.create(
                        log_id = "UL0" + str(all_userLogs + 1),
                        activity = "Edit User",
                        username = request.user,
                        audit_details = str(request.user) + " updated user " + employeeID + "'s details.",
                        audit_type = 1
                        )
                        add_log.save()

                        messages.success(request, f'Updated user {employeeID} successfully!')
                        return redirect('masterlist')
                
                messages.error(request, f'Cannot find {employeeID}.')
                return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')
    
def del_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            employeeID = request.POST.get("username")

            all_users = User.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

            for user in all_users:
                if user.username == employeeID:
                    user.profile.is_deleted = True
                    user.is_active = False
                    deladmin_mail(user.email)
                    user.save()

                    add_log = AuditLogs.objects.create(
                        log_id = "UL0" + str(all_userLogs + 1),
                        activity = "Delete User",
                        username = request.user,
                        audit_details = str(request.user) + " deleted user " + employeeID + " from the system.",
                        audit_type = 1
                    )
                    add_log.save()
                    messages.success(request, f'Deleted user {employeeID} successfully!')
                    return redirect('masterlist')
            
            messages.error(request, f'Cannot find {employeeID}.')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_admin(request):
    if request.user.is_authenticated: 
        if request.method == 'POST':
            context = {}
            print(request.POST.get("username"))
            context['username'] = request.POST.get("username")
            context['all_users'] = User.objects.all()
            context['job_positions'] = JobPosition.objects.all()
        return render(request, 'MASTERLIST-EditAdmin.html', context = context)
    else:
        return render(request, 'AEIRBS-Login.html')
   
def add_admin(request):
    if request.user.is_authenticated:
        JOB_POSITIONS = JobPosition.objects.all()
        return render(request, 'MASTERLIST-AddAdmin.html', {'job_positions': JOB_POSITIONS})
    else:
        return render(request, 'AEIRBS-Login.html')

def delete_list(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            all_users = User.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
            admin_list = request.POST.get('delete_list')
            for user in all_users:
                if user.username in admin_list:
                    user.profile.is_deleted = True
                    user.is_active = False
                    deladmin_mail(user.email)
                    user.save()

            add_log = AuditLogs.objects.create(
                log_id = "UL0" + str(all_userLogs + 1),
                activity = "Delete Users",
                username = request.user,
                audit_details = str(request.user) + " deleted users from the system.",
                audit_type = 1
            )
            add_log.save()

            messages.success(request, f'Users deleted successfully!')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def add_position(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
            all_positions = JobPosition.objects.filter(position_isDeleted = False)

            #Get User Input
            add_jobPosition = request.POST.get("addJobPosition")

            #Validate User Input
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
            if not add_jobPosition.strip():
                errors["error_jobPositionEmpty"] = "Job Position is required."
            else:
                if not validate_stringFormat(add_jobPosition):
                    errors["error_jobPositionFormat"] = "Invalid, input should only contain letters."

            context['all_positions'] = all_positions
            context['inputJobPosition'] = add_jobPosition
            context['errors'] = errors

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'SETTINGS-Devices.html',  context = context)
            else:
                #Format User Input
                add_jobPosition = format_input(add_jobPosition)

                #Add Job Position
                position = JobPosition.objects.create(
                    job_position = add_jobPosition
                )
                position.save()

                #Create User Log
                add_log = AuditLogs.objects.create(
                    log_id = "UL0" + str(all_userLogs + 1),
                    activity = "Add Job Position",
                    username = request.user,
                    audit_details = str(request.user) + " add new job position.",
                    audit_type = 1
                )
                add_log.save()

                messages.success(request, f'Job Position added successfully!')
                return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_position(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            errors = {}

            all_positions = JobPosition.objects.filter(position_isDeleted = False)
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

            #Get User Input
            edit_jobPositionID = int(request.POST.get("editJobPositionID"))
            edit_jobPosition = format_input(request.POST.get("editJobPosition"))

            #Validate User Input
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
            if not edit_jobPosition.strip():
                errors["error_editJobPositionEmpty"] = "Job Position is required."
            else:
                if not validate_stringFormat(edit_jobPosition):
                    errors["error_editJobPositionFormat"] = "Invalid, input should only contain letters."

            context['all_positions'] = all_positions
            context['inputJobPositionID'] = edit_jobPositionID
            context['inputJobPosition'] = edit_jobPosition
            context['errors'] = errors
            context['error'] = True

            if len(errors) > 0:
                messages.error(request, f'Invalid Input!')  
                return render(request, 'SETTINGS-Devices.html',  context = context)
            else:
                #Format User Input
                edit_jobPosition = format_input(edit_jobPosition)

                #Update Job Position
                for position in all_positions:
                    if position.id == edit_jobPositionID:
                        jobPosition = position.job_position
                        position.job_position = edit_jobPosition
                        position.save()

                        #Create User Log
                        add_log = AuditLogs.objects.create(
                            log_id = "UL0" + str(all_userLogs + 1),
                            activity = "Edit Job Position",
                            username = request.user,
                            audit_details = str(request.user) + " updated " + jobPosition + " to " + edit_jobPosition + ".",
                            audit_type = 1
                        )
                        add_log.save()

                        messages.success(request, f'Updated {jobPosition} to {edit_jobPosition} successfully!')
                        return redirect('devices')
            
                messages.error(request, f'Job Position not found!')
                return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')

def delete_position(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            all_positions = JobPosition.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

            #Get User Input
            delete_jobPosition = int(request.POST.get("deleteJobPositionID"))

            #Delete Job Position
            for position in all_positions:
                if position.id == delete_jobPosition:
                    jobPosition = position.job_position
                    position.position_isDeleted = True
                    position.save()

                    #Create User Log
                    add_log = AuditLogs.objects.create(
                        log_id = "UL0" + str(all_userLogs + 1),
                        activity = "Delete Job Position",
                        username = request.user,
                        audit_details = str(request.user) + " deleted " + jobPosition + ".",
                        audit_type = 1
                        )
                    add_log.save()

                    messages.success(request, f'Deleted {jobPosition} successfully!')
                    return redirect('devices')

        messages.error(request, f'Job Position not found!')
        return redirect('devices')
    else:
        return render(request, 'AEIRBS-Login.html')
 
            

 