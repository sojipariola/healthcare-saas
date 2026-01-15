from django.db import models
from tenants.models import Tenant

class AnalyticsEvent(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=64)
    user_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.event_type} at {self.timestamp} (tenant {self.tenant_id})"
