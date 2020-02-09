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
    path('home/', components_views.home, name='home'),
    path('masterlist/', accounts_views.masterlist, name='masterlist'),
    path('audit/', reports_views.audit, name='audit'),
    path('incident/', reports_views.incident, name='incident'),
    path('summary/', reports_views.summary, name='summary'),
    path('profile/', accounts_views.profile, name='profile'),
    path('admin/', admin.site.urls),

    # URL Actions
    path('add-user/', accounts_views.add_user, name='add_user'),
    path('del-user/', accounts_views.del_user, name='del_user'),
    # path('edit-user/', accounts_views.edit_user, name='edit_user'),
    # path('add-comp/', components_views.add_comp, name='add_comp'),
    # path('del-comp/', components_views.del_comp, name='del_comp'),
    # path('update-comp/', components_views.update_comp, name='update_comp'),
    path('login/', accounts_views.login_action, name='login_action'),
    path('logout/', accounts_views.logout_action, name='logout_action'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
