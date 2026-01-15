

from django.db import models
from patients.models import Patient
from tenants.models import Tenant

class LabResult(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="lab_results")
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="lab_results")
	result = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"LabResult for {self.patient} at {self.created_at}"
