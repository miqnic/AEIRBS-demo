from django.shortcuts import render
from django.http import HttpResponseRedirect

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
        audit_logs = AuditLogs.objects.all().order_by('-username')
        return render(request, "AEIRBS-Audit.html", {'audit_logs': audit_logs})
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def generatePDF_audit(request):
    if request.user.is_authenticated and request.user.is_superuser:
        audit_logs = AuditLogs.objects.all().order_by('id')
        context = {}
        dateTime = datetime.datetime.now()
        context['audit_logs'] = audit_logs
        
        pdf = renderPDF('reports/generatePDF-audit.html', context)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Audit-Reports-%s.pdf" %(dateTime)
        content = "attachment; filename='%s'" %(filename)
        response['Content-Disposition'] = content
        return response

        #return render(request, "AEIRBS-Audit.html", {'audit_logs': audit_logs})
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
