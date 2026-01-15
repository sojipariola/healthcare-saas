from django import forms
from .models import ClinicalRecord

class ClinicalRecordForm(forms.ModelForm):
    class Meta:
        model = ClinicalRecord
        fields = ["patient", "note"]
