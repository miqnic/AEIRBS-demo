from django.db import models
from django.conf import settings

from components.models import Device_Sensor
from .utils import IncidentCombinations, IncidentLevels

# Create your models here.
AUDIT_TYPE= [
    (0, 'Component Logs'),
    (1, 'User Logs'),
    (2, 'Maintenance Logs')
]

class AuditLogs(models.Model):
    log_id = models.CharField(max_length=15, unique=True)
    activity = models.CharField(max_length=100)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    date_time = models.DateTimeField(auto_now_add=True)
    audit_details = models.CharField(max_length=100, default='details')
    audit_type = models.IntegerField(choices=AUDIT_TYPE)
    audit_isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.log_id)

class Incident(models.Model):
    incident_type = models.CharField(
        max_length=25,
        choices=IncidentCombinations.choices(),
        default=IncidentCombinations.FR,
    )

    def __str__(self):
        return self.incident_type

class IncidentReport(models.Model):
    device_sensor_id = models.ForeignKey(Device_Sensor, on_delete=models.DO_NOTHING)
    incident_type = models.ForeignKey(Incident, on_delete=models.DO_NOTHING)
    incident_date_time = models.DateTimeField(auto_now_add=True)
    incident_level = models.CharField(
        max_length=20,
        choices=IncidentLevels.choices(),
        default=IncidentLevels.FR_FIRST,
    )

    def __str__(self):
        return str(self.incident_date_time)