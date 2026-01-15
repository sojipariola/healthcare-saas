from django.db import models
from patients.models import Patient
from users.models import CustomUser
from referrals.models import Referral

class Document(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    referral = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.file.name} for {self.patient}"