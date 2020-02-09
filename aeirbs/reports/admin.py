from django.contrib import admin

from .models import AuditLogs, Incident, IncidentReport

# Register your models here.

admin.site.register(AuditLogs)
admin.site.register(Incident)
admin.site.register(IncidentReport)