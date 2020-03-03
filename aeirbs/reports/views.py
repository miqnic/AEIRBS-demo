from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import AuditLogs, IncidentReport

# Create your views here.

def audit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all().order_by('-username')
        return render(request, "AEIRBS-Audit.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def incident(request):
    if request.user.is_authenticated:
        incident_reports = IncidentReport.objects.all()
        return render(request, "AEIRBS-Incident.html", {'incident_reports': incident_reports})
    else:
        return render(request, 'AEIRBS-Login.html')

def summary(request):
    if request.user.is_authenticated:
        return render(request, "AEIRBS-Summary.html")
    else:
        return render(request, 'AEIRBS-Login.html')
