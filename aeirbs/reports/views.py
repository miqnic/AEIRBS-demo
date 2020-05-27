from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import AuditLogs, IncidentReport
from components.models import Device
  
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractMonth, ExtractYear
from .utils import IncidentCombinations, IncidentLevels

import datetime
import calendar
import pandas as pd
from datetime import date, timedelta
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
        context = {}
        context['all_devices'] = Device.objects.all()
        context['audit_logs'] = AuditLogs.objects.all()
        return render(request, "AEIRBS-Audit.html", context=context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def component_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        context['all_devices'] = Device.objects.all().filter(device_isDeleted=False)
        audit_logs = AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False)

        if request.method == 'POST':
            keyword = request.POST.get("keyword")
            audit_logs = AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False, activity__contains = keyword) | AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False, username__first_name__contains = keyword) | AuditLogs.objects.filter(audit_type = 0, audit_isDeleted = False, username__last_name__contains = keyword)

        context['audit_logs'] = audit_logs

        return render(request, "AUDIT-ComponentLogs.html", context = context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def user_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        context['all_devices'] = Device.objects.all().filter(device_isDeleted=False)
        audit_logs = AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False)

        if request.method == 'POST':
            keyword = request.POST.get("keyword")
            audit_logs = AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False, activity__contains = keyword) | AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False, username__first_name__contains = keyword) | AuditLogs.objects.filter(audit_type = 1, audit_isDeleted = False, username__last_name__contains = keyword)

        context['audit_logs'] = audit_logs

        return render(request, "AUDIT-UserLogs.html", context = context)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def maintenance_logs(request):
    if request.user.is_authenticated and request.user.is_superuser:
        context = {}
        context['all_devices'] = Device.objects.all().filter(device_isDeleted=False)
        audit_logs = AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False)

        if request.method == 'POST':
            keyword = request.POST.get("keyword")
            audit_logs = AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False, activity__contains = keyword) | AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False, username__first_name__contains = keyword) | AuditLogs.objects.filter(audit_type = 2, audit_isDeleted = False, username__last_name__contains = keyword)

        context['audit_logs'] = audit_logs

        return render(request, "AUDIT-MaintenanceLogs.html", context = context)
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
        context = {}
        context['all_devices'] = Device.objects.all().filter(device_isDeleted=False)
        context['incident_reports'] = IncidentReport.objects.all()
        return render(request, "AEIRBS-Incident.html", context = context)
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
        context = {}
        context['all_devices'] = Device.objects.all().filter(device_isDeleted=False)
        return render(request, "AEIRBS-Summary.html", context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

def generate_summary(request):
    if request.user.is_authenticated:
        dates = request.POST.get('dateRange').split('-')
        start = dates[0].split('/')
        end = dates[1].split('/')
        startday = int(start[1])
        startmos = int(start[0])
        startyr = int(start[2])
        endday = int(end[1])
        endmos = int(end[0])
        endyr = int(end[2])
        sdate = date(startyr, startmos, startday)   # start date
        edate = date(endyr, endmos, endday)   # end date

        all_incidents = IncidentReport.objects.filter(incident_date_time__gte=datetime.date(startyr, startmos, startday),
                                incident_date_time__lte=datetime.date(endyr, endmos, endday))

        eq_incidents = all_incidents.filter(incident_type_id=1)
        fr_incidents = all_incidents.filter(incident_type_id=2)
        fl_incidents = all_incidents.filter(incident_type_id=3)

        all_query = all_incidents.annotate(month=ExtractMonth('incident_date_time'),year=ExtractYear('incident_date_time')).values('month', 'year').annotate(count=Count('month'))
        eq_query = eq_incidents.annotate(month=ExtractMonth('incident_date_time'),year=ExtractYear('incident_date_time')).values('month', 'year').annotate(count=Count('month'))
        fr_query = fr_incidents.annotate(month=ExtractMonth('incident_date_time'),year=ExtractYear('incident_date_time')).values('month', 'year').annotate(count=Count('month'))
        fl_query = fl_incidents.annotate(month=ExtractMonth('incident_date_time'),year=ExtractYear('incident_date_time')).values('month', 'year').annotate(count=Count('month'))

        #eqlvl_query = eq_incidents.order_by('incident_level').annotate(count = Count('incident_level'))
        eqlvl_query = eq_incidents.values('incident_level').annotate(count=Count('incident_level')).order_by('count')
        frlvl_query = fr_incidents.values('incident_level').annotate(count=Count('incident_level')).order_by('count')
        fllvl_query = fl_incidents.values('incident_level').annotate(count=Count('incident_level')).order_by('count')

        print(eqlvl_query)

        eq_months = []
        fr_months = []
        fl_months = []
        eq_count = []
        fr_count = []
        fl_count = []
        months = []

        eq_total = []
        fr_total = []
        fl_total = []

        eq_lvls = []
        fr_lvls = []
        fl_lvls = []
        eq_cntlvl = []
        fr_cntlvl = []
        fl_cntlvl = []

        for eqlvl in eqlvl_query:
            eq_lvls.append(eqlvl['incident_level'])
            eq_cntlvl.append(eqlvl['count'])
        
        for frlvl in frlvl_query:
            fr_lvls.append(frlvl['incident_level'])
            fr_cntlvl.append(frlvl['count'])

        for fllvl in fllvl_query:
            fl_lvls.append(fllvl['incident_level'])
            fl_cntlvl.append(fllvl['count'])

        for all in all_query:
            months.append(calendar.month_abbr[all['month']] + " " + str(all['year']))

        for eq in eq_query:
            month_key = calendar.month_abbr[eq['month']] + " " + str(eq['year'])
            eq_months.append(month_key)
            eq_count.append(eq["count"])
        
        for fl in fl_query:
            month_key = calendar.month_abbr[fl['month']] + " " + str(fl['year'])
            fl_months.append(month_key)
            fl_count.append(fl["count"])
        
        for fr in fr_query:
            month_key = calendar.month_abbr[fr['month']] + " " + str(fr['year'])
            fr_months.append(month_key)
            fr_count.append(fr["count"])
        
        

        intctr = 0
        for mos in months:
            if mos in eq_months:
                eq_total.append(eq_count[intctr])
                intctr+=1
            else:
                eq_total.append(0)
        
        intctr = 0
        for mos in months:
            if mos in fl_months:
                fl_total.append(fl_count[intctr])
                intctr+=1
            else:
                fl_total.append(0)

        intctr = 0
        for mos in months:
            if mos in fr_months:
                fr_total.append(fr_count[intctr])
                intctr+=1
            else:
                fr_total.append(0)

        

        context = {'months':months, 'eq_lvls': eq_lvls, 'eq_cntlvl': eq_cntlvl, 'eq_months': eq_months, 'eq_total': eq_total, 'fr_lvls': fr_lvls, 'fr_cntlvl': fr_cntlvl, 'fr_months': fr_months,'fr_total': fr_total, 'fl_lvls': fl_lvls, 'fl_cntlvl': fl_cntlvl, 'fl_months': fl_months, 'fl_total': fl_total}

        context['all_devices'] = Device.objects.all().filter(device_isDeleted=False)

        return render(request, "AEIRBS-Summary.html", context = context)
    else:
        return render(request, 'AEIRBS-Login.html')

        
        
