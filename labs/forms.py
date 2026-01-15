from django import forms
from .models import LabResult

class LabResultForm(forms.ModelForm):
    class Meta:
        model = LabResult
        fields = ["patient", "result"]
