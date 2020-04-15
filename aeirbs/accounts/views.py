from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from reports.models import AuditLogs
from .models import Profile

# Create your views here.

def login_action(request):
    if request.method == 'POST':
        username = request.POST.get("company_id")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            # Log: Logged In - Valid User
            log = AuditLogs(
                activity="Login",
                username = request.user
            )
            log.save()

            messages.success(request, f'Login is successful!')
            return redirect('earthquake_components')
        else:
            messages.error(request, f'Invalid credentials.')
            return redirect('login_page')

def logout_action(request):
    # Log: Logged Out
    log = AuditLogs(
        activity="Logout",
        username = request.user
    )
    log.save()

    logout(request)
    return redirect('login_page')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('earthquake_components')
    else:
        return render(request, 'AEIRBS-Login.html')

def masterlist(request):
    users = User.objects.all().filter(profile__is_deleted=False)
    audit_logs = AuditLogs.objects.all()
    logs = []

    for audit in audit_logs:
        temp = (str(audit.username), audit.activity, audit.date_time,  audit.details)
        logs.append(temp)

    return render(request, 'AEIRBS-Masterlist.html', {'users': users, 'logs': logs})

def add_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            employee_id = request.POST.get("inputEmployeeID")
            email = request.POST.get("inputCompanyEmail")
            first_name = request.POST.get("inputFirstName")
            middle_name = request.POST.get("inputMiddleName")
            last_name = request.POST.get("inputLastName")

            if request.POST.get("accessRole") == "adminRole":
                is_super = False
            else:
                is_super = True

            user = User.objects.create_user(
                username=employee_id,
                password="default123",
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_superuser=is_super,
                is_staff=is_super
            )
            user.save()
            user.refresh_from_db()
            user.profile.middle_name = middle_name
            user.save()

            messages.success(request, f'Added user {first_name} {last_name} successfully!')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')
    
def del_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            employee_id = request.POST.get("username")

            users = User.objects.all()

            log = AuditLogs(
                activity="Delete",
                username = request.user,
                details= "User " + str(request.user) + " deleted user " + employee_id + " from the system."  
            )

            log.save()

            for user in users:
                if user.username == employee_id:
                    user.profile.is_deleted = True
                    user.is_active = False
                    user.save()
                    messages.success(request, f'Removed user {user.first_name} {user.last_name} successfully!')
                    return redirect('masterlist')
            
            messages.error(request, f'Cannot find {employee_id}.')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            userid = request.POST.get("username")
            employee_id = request.POST.get("employeeID")
            first_name = request.POST.get("firstName")
            middle_name = request.POST.get("middleName")
            last_name = request.POST.get("lastName")
            company_email =request.POST.get("companyEmail")
            job_position =request.POST.get("jobPosition")
            mobile_number =request.POST.get("mobileNumber")

            users = User.objects.all()

            for user in users:
                if user.username == userid:
                    user.username = employee_id
                    user.first_name = first_name
                    user.profile.middle_name = middle_name
                    user.last_name = last_name
                    user.email = company_email
                    user.profile.job_title = job_position
                    user.profile.phone_number = mobile_number
                    user.save()
                    messages.success(request, f'updated user {user.first_name} {user.last_name} successfully!')
                    return redirect('masterlist')
            
            messages.error(request, f'Cannot find user.')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def profile(request):
    audit_logs = AuditLogs.objects.all()
    logs = []

    for audit in audit_logs:
        temp = (str(audit.username), audit.activity, audit.date_time, audit.details)
        logs.append(temp)

    return render(request, 'AEIRBS-Profile.html', {'logs': logs})


