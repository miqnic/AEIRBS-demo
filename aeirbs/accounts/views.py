from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from reports.models import AuditLogs
from .models import Profile, DEFAULT_IMAGE
from django.core.files.storage import FileSystemStorage

# Create your views here.

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("company_id")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

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
        return render(request, 'AEIRBS-Login.html')

def masterlist(request):
    context = {}
    context['users'] = User.objects.all().filter(profile__is_deleted=False)
    context['logs'] = AuditLogs.objects.all()

    if request.method == 'POST':
        keyword = request.POST.get("keyword")
        context['users'] = User.objects.filter(profile__is_deleted=False, username__contains = keyword) | User.objects.filter(profile__is_deleted=False, first_name__contains = keyword) | User.objects.filter(profile__is_deleted=False, profile__middle_name__contains = keyword) | User.objects.filter(profile__is_deleted=False, last_name__contains = keyword)
    
    return render(request, 'AEIRBS-Masterlist.html', context = context)

def add_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            context = {}
            add_employeeID = request.POST.get("addAdminEmployeeID")
            add_firstName = request.POST.get("addAdminFirstName")
            add_middleName = request.POST.get("addAdminMiddleName")
            add_lastName = request.POST.get("addAdminLastName")
            add_jobPosition = request.POST.get("addAdminJobPosition")
            add_companyEmail = request.POST.get("addAdminCompanyEmail")
            add_mobileNumber = request.POST.get("addAdminMobileNumber")
            add_userImage = request.FILES.get("addAdminImage")

            if request.POST.get("addAdminAccessRole") == "adminRole":
                is_super = False
            else:
                is_super = True

            context["inputAccessRole"] = is_super
            context["inputEmployeeID"] = add_employeeID
            context["inputFirstName"] = add_firstName
            context["inputMiddleName"] = add_middleName
            context["inputLastName"] = add_lastName
            context["inputJobPosition"] = add_jobPosition
            context["inputMobileNumber"] = add_mobileNumber
            context["inputCompanyEmail"] = add_companyEmail

            if add_userImage == None:
                add_userImage = DEFAULT_IMAGE

            all_users = User.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()
            isExisting = False
            for user in all_users:
                if user.username == add_employeeID:
                    isExisting = True
            
            if isExisting:
                messages.error(request, f'{add_employeeID} is already registered in the system!')  
                return render(request, 'MASTERLIST-AddAdmin.html', context = context)
            else:
                add_admin = User.objects.create_user(
                    username = add_employeeID,
                    password= add_employeeID,
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
                    user.save()

                    add_log = AuditLogs.objects.create(
                    log_id = "UL0" + str(all_userLogs + 1),
                    activity = "Delete User",
                    username = request.user,
                    audit_details = str(request.user) + " deleted uder " + employeeID + " from the system.",
                    audit_type = 1
                    )
                    add_log.save()
                    messages.success(request, f'Deleted user {employeeID} successfully!')
                    return redirect('masterlist')
            
            messages.error(request, f'Cannot find {employeeID}.')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
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

            all_users = User.objects.all()
            all_userLogs = AuditLogs.objects.filter(audit_type = 1).count()

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

def edit_admin(request):
    if request.user.is_authenticated:
        return render(request, 'MASTERLIST-EditAdmin.html')
    else:
        return render(request, 'AEIRBS-Login.html')
   
def add_admin(request):
    if request.user.is_authenticated:
        return render(request, 'MASTERLIST-AddAdmin.html')
    else:
        return render(request, 'AEIRBS-Login.html')

