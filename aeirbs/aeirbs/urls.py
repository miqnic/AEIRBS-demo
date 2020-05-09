"""aeirbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from components import views as components_views
from accounts import views as accounts_views
from reports import views as reports_views

urlpatterns = [
    # URL Pages
    # Admin Page will be removed when it is to be deployed
    path('', accounts_views.login_page, name='login_page'), 
    #path('home/', components_views.home, name='home'),
    path('masterlist/', accounts_views.masterlist, name='masterlist'),
    path('audit/', reports_views.audit, name='audit'),
    path('incident/', reports_views.incident, name='incident'),
    path('summary/', reports_views.summary, name='summary'),
    path('edit-admin/', accounts_views.edit_admin, name='edit_admin'),
    path('admin/', admin.site.urls),
    
    # Add Component Path
    path('add-component/', components_views.add_component, name='add_component'),

    # URL Actions
    path('add-admin/', accounts_views.add_admin, name='add_admin'),
    path('add-user/', accounts_views.add_user, name='add_user'),
    path('del-user/', accounts_views.del_user, name='del_user'),
    path('edit-user/', accounts_views.edit_user, name='edit_user'),
        
    path('generate-audit/', reports_views.generatePDF_audit, name='generatePDF_audit'),
    path('generate-incident/', reports_views.generatePDF_incident, name='generatePDF_incident'),

    # path('edit-user/', accounts_views.edit_user, name='edit_user'),



    # path('del-comp/', components_views.del_comp, name='del_comp'),
    # path('update-comp/', components_views.update_comp, name='update_comp'),
    path('login/', accounts_views.login_action, name='login_action'),
    path('logout/', accounts_views.logout_action, name='logout_action'),

    # DASHBOARD Components
    path('dashboard/earthquake-components/', components_views.earthquake_components, name='earthquake_components'),
    path('dashboard/fire-components/', components_views.fire_components, name='fire_components'),
    path('dashboard/flood-components/', components_views.flood_components, name='flood_components'),
    path('dashboard/devices/', components_views.devices, name='devices'),
    path('dashboard/sensors/', components_views.sensors, name='sensors'),
    # CRUD Actions
    path('add-device/', components_views.add_device, name='add_device'),
    path('add-sensor/', components_views.add_sensor, name='add_sensor'),
    path('add-comp/', components_views.add_comp, name='add_comp'),

    path('edit-device/', components_views.edit_device, name='edit_device'),
    path('edit-sensor/', components_views.edit_sensor, name='edit_sensor'),
    path('edit-comp/', components_views.edit_comp, name='edit_comp'),
    path('status/', components_views.status, name='status'),

    path('delete-device/', components_views.del_device, name='del_device'),
    path('delete-sensor/', components_views.del_sensor, name='del_sensor'),
    path('delete-comp/', components_views.del_comp, name='del_comp'),
    # SEARCH Function
    path('search-component/', components_views.search_component, name='search_component'),


    # AUDIT Logs
    path('audit/component-logs/', reports_views.component_logs, name='component_logs'),
    path('audit/user-logs/', reports_views.user_logs, name='user_logs'),
    path('audit/maintenance-logs/', reports_views.maintenance_logs, name='maintenance_logs'),

    path('audit/component-logs/clear-logs/', reports_views.clear_componentLogs, name='clear_componentLogs'),
    path('audit/user-logs/clear-logs/', reports_views.clear_userLogs, name='clear_userLogs'),
    path('audit/maintenance-logs/clear-logs/', reports_views.clear_maintenanceLogs, name='clear_maintenanceLogs'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
