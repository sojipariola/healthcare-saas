from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from referrals.models import CLINIC_TYPES
from .clinic_note_types import CLINIC_NOTE_TEMPLATES
from .models import ClinicalRecord
from tenants.models import Tenant

@login_required
def clinic_note_create(request):
    patients = Patient.objects.filter(tenant=request.user.tenant)
    clinic_types = CLINIC_TYPES
    template = []
    values = {}
    patient_id = None
    clinic_type = None
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        clinic_type = request.POST.get("clinic_type")
        template = CLINIC_NOTE_TEMPLATES.get(clinic_type, [])
        for idx, section in enumerate(template, 1):
            values[section] = request.POST.get(f"section_{idx}", "")
        note_text = "\n\n".join(f"{section}:\n{values[section]}" for section in template)
        if patient_id and clinic_type:
            ClinicalRecord.objects.create(
                tenant=request.user.tenant,
                patient_id=patient_id,
                note=note_text
            )
            return redirect("clinicalrecord_list")
    elif request.method == "GET" and request.GET.get("clinic_type"):
        clinic_type = request.GET.get("clinic_type")
        template = CLINIC_NOTE_TEMPLATES.get(clinic_type, [])
    return render(request, "clinical_records/clinic_note_form.html", {
        "patients": patients,
        "clinic_types": clinic_types,
        "template": template,
        "values": values,
        "patient_id": patient_id,
        "clinic_type": clinic_type,
    })
