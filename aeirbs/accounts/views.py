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
            return redirect('home')
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
        return redirect('home')
    else:
        return render(request, 'AEIRBS-Login.html')

def masterlist(request):
    users = User.objects.all().filter(profile__is_deleted=False)
    return render(request, 'AEIRBS-Masterlist.html', {'users': users})

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
            employee_id = request.POST.get("inputEmployeeID")

            users = User.objects.all()

            for user in users:
                if user.username == employee_id:
                    user.profile.is_deleted = True
                    user.is_active = False
                    user.save()
                    messages.success(request, f'Removed user {user.first_name} {user.last_name} successfully!')
                    return redirect('masterlist')
            
            messages.error(request, f'Cannot find user.')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def edit_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            employee_id = request.POST.get("inputEmployeeID")
            employee_id = request.POST.get("inputEmployeeID")
            email = request.POST.get("inputCompanyEmail")
            first_name = request.POST.get("inputFirstName")
            middle_name = request.POST.get("inputMiddleName")
            last_name = request.POST.get("inputLastName")

            users = User.objects.all()

            for user in users:
                if user.username == employee_id:
                    user.profile.is_deleted = True
                    user.save()
                    messages.success(request, f'Removed user {user.first_name} {user.last_name} successfully!')
                    return redirect('masterlist')
            
            messages.error(request, f'Cannot find user.')
            return redirect('masterlist')
    else:
        return render(request, 'AEIRBS-Login.html')

def profile(request):
    return render(request, 'AEIRBS-Profile.html')


