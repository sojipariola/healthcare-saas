

from django.db import models
from patients.models import Patient
from tenants.models import Tenant

class ClinicalRecord(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="clinical_records")
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="clinical_records")
	note = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Record for {self.patient} at {self.created_at}"
