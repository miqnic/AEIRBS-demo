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
        audit_logs = AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False)

        if request.method == 'POST':
            keyword = request.POST.get("keyword")
            audit_logs = AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False, activity__contains = keyword) | AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False, username__first_name__contains = keyword) | AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False, username__last_name__contains = keyword)

        return render(request, "AUDIT-ComponentLogs.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False)

        if request.method == 'POST':
            keyword = request.POST.get("keyword")
            audit_logs = AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False, activity__contains = keyword) | AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False, username__first_name__contains = keyword) | AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False, username__last_name__contains = keyword)

        return render(request, "AUDIT-UserLogs.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def maintenance_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False)

        if request.method == 'POST':
            keyword = request.POST.get("keyword")
            audit_logs = AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False, activity__contains = keyword) | AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False, username__first_name__contains = keyword) | AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False, username__last_name__contains = keyword)

        return render(request, "AUDIT-MaintenanceLogs.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def clear_logs(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            audit_type = int(request.POST.get("clearAuditType"))
            audit_logs = AuditLogs.objects.filter(audit_type = audit_type, audit_isDeleted = False)
            for log in audit_logs:
                log.audit_isDeleted = True
                log.save()
            if audit_type == 0:
                log_count = AuditLogs.objects.filter(audit_type = audit_type).count()
                add_log = AuditLogs.objects.create(
                    log_id = "CL0" + str(log_count + 1),
                    activity = "Clear Component Logs",
                    username = request.user,
                    audit_details = str(request.user) + " cleared all Component Logs from the system.",
                    audit_type = audit_type
                )
                add_log.save()
                audit_logs = AuditLogs.objects.filter(audit_type = audit_type, audit_isDeleted = False) 
                messages.success(request, f'Cleared Component Logs successfully!')
                return render(request, "AUDIT-ComponentLogs.html", {'audit_logs': audit_logs})
            if audit_type == 1:
                log_count = AuditLogs.objects.filter(audit_type = audit_type).count()
                add_log = AuditLogs.objects.create(
                    log_id = "UL0" + str(log_count + 1),
                    activity = "Clear User Logs",
                    username = request.user,
                    audit_details = str(request.user) + " cleared all User Logs from the system.",
                    audit_type = audit_type
                )
                add_log.save()
                audit_logs = AuditLogs.objects.filter(audit_type = audit_type, audit_isDeleted = False) 
                messages.success(request, f'Cleared User Logs successfully!')
                return render(request, "AUDIT-UserLogs.html", {'audit_logs': audit_logs})
            if audit_type == 2:
                log_count = AuditLogs.objects.filter(audit_type = audit_type).count()
                add_log = AuditLogs.objects.create(
                    log_id = "ML0" + str(log_count + 1),
                    activity = "Clear Maintenance Logs",
                    username = request.user,
                    audit_details = str(request.user) + " cleared all Maintenance Logs from the system.",
                    audit_type = audit_type
                )
                add_log.save()
                audit_logs = AuditLogs.objects.filter(audit_type = audit_type, audit_isDeleted = False) 
                messages.success(request, f'Cleared Maintenance Logs successfully!')
                return render(request, "AUDIT-MaintenanceLogs.html", {'audit_logs': audit_logs})
    else:
        return render(request, 'AEIRBS-Login.html')

def generatePDF_audit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            auditType = int(request.POST.get("auditType"))
            audit_logs = AuditLogs.objects.filter(audit_type = auditType)
            dateTime = datetime.datetime.now()
            date = dateTime.strftime("%x")
            time = dateTime.strftime("%X")
            context = {}

            context['audit_type'] = auditType
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
