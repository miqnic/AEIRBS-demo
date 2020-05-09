from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import AuditLogs, IncidentReport
  
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

import datetime
# Create your views here.

def renderPDF(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def audit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all()
        return render(request, "AEIRBS-Audit.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def component_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all().filter(audit_type = 0)
        return render(request, "AUDIT-ComponentLogs.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all().filter(audit_type = 1)
        return render(request, "AUDIT-UserLogs.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def maintenance_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all().filter(audit_type = 2)
        return render(request, "AUDIT-MaintenanceLogs.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def clear_componentLogs(request):
    if request.user.is_authenticated:
        if AuditLogs.objects.filter(audit_type = 0).count() > 0:
            AuditLogs.objects.filter(audit_type = 0).delete()
            audit_logs = AuditLogs.objects.all().filter(audit_type = 0)
            messages.success(request, f'Cleared Component Logs successfully!')
            return render(request, "AUDIT-ComponentLogs.html", {'audit_logs': audit_logs})
        else:
            audit_logs = AuditLogs.objects.all().filter(audit_type = 0)
            messages.error(request, f'Component Logs is Empty!')
            return render(request, "AUDIT-ComponentLogs.html", {'audit_logs': audit_logs})
    else:
        return render(request, 'AEIRBS-Login.html')

def clear_userLogs(request):
    if request.user.is_authenticated:
        if AuditLogs.objects.filter(audit_type = 1).count() > 0:
            AuditLogs.objects.filter(audit_type = 1).delete()
            audit_logs = AuditLogs.objects.all().filter(audit_type = 1)
            messages.success(request, f'Cleared User Logs successfully!')
            return render(request, "AUDIT-UserLogs.html", {'audit_logs': audit_logs})
        else:
            audit_logs = AuditLogs.objects.all().filter(audit_type = 1)
            messages.error(request, f'User Logs is Empty!')
            return render(request, "AUDIT-UserLogs.html", {'audit_logs': audit_logs})
    else:
        return render(request, 'AEIRBS-Login.html')

def clear_maintenanceLogs(request):
    if request.user.is_authenticated:
        if AuditLogs.objects.filter(audit_type = 2).count() > 0:
            AuditLogs.objects.filter(audit_type = 2).delete()
            audit_logs = AuditLogs.objects.all().filter(audit_type = 2)
            messages.success(request, f'Cleared Maintenance Logs successfully!')
            return render(request, "AUDIT-MaintenanceLogs.html", {'audit_logs': audit_logs})
        else:
            audit_logs = AuditLogs.objects.all().filter(audit_type = 2)
            messages.error(request, f'Maintenance Logs is Empty!')
            return render(request, "AUDIT-MaintenanceLogs.html", {'audit_logs': audit_logs})
    else:
        return render(request, 'AEIRBS-Login.html')

def generatePDF_audit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all()
        dateTime = datetime.datetime.now()
        date = dateTime.strftime("%x")
        time = dateTime.strftime("%X")
        context = {}

        context['audit_logs'] = audit_logs.reverse()
        context['date'] = date
        context['time'] = time
        
        pdf = renderPDF('reports/generatePDF-audit.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Audit-Reports-%s.pdf" %(dateTime)
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not Found")    
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def incident(request):
    if request.user.is_authenticated:
        incident_reports = IncidentReport.objects.all()
        return render(request, "AEIRBS-Incident.html", {'incident_reports': incident_reports})
    else:
        return render(request, 'AEIRBS-Login.html')

def generatePDF_incident(request):
    if request.user.is_authenticated and request.user.is_superuser:
        incident_id = request.POST.get("download_incident")
        incident_reports = IncidentReport.objects.filter(id=incident_id)
        dateTime = datetime.datetime.now()
        date = dateTime.strftime("%x")
        time = dateTime.strftime("%X")
        context = {}

        context['incident_reports'] = incident_reports
        context['date'] = date
        context['time'] = time

        for report in incident_reports:
            print(report.incident_type)
        
        pdf = renderPDF('reports/generatePDF-incident.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Incident-Reports-%s.pdf" %(dateTime)
            content = "inline; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not Found")    
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def summary(request):
    if request.user.is_authenticated:
        return render(request, "AEIRBS-Summary.html")
    else:
        return render(request, 'AEIRBS-Login.html')
