
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import ClinicalRecord
from patients.models import Patient
from .forms import ClinicalRecordForm
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('clinical_records.change_clinicalrecord', raise_exception=True)
def clinicalrecord_edit(request, pk):
	record = get_object_or_404(ClinicalRecord, pk=pk)
	if request.method == "POST":
		form = ClinicalRecordForm(request.POST, instance=record)
		if form.is_valid():
			form.save()
			return redirect(reverse("clinicalrecord_detail", args=[record.pk]))
	else:
		form = ClinicalRecordForm(instance=record)
	return render(request, "clinical_records/clinicalrecord_form.html", {"form": form, "edit": True})

@login_required
@permission_required('clinical_records.delete_clinicalrecord', raise_exception=True)
def clinicalrecord_archive(request, pk):
	record = get_object_or_404(ClinicalRecord, pk=pk)
	if request.method == "POST":
		record.note = "[ARCHIVED] " + record.note
		record.save()
		return redirect(reverse("clinicalrecord_list"))
	return render(request, "clinical_records/clinicalrecord_confirm_archive.html", {"record": record})

@login_required
def clinicalrecord_list(request):
	records = ClinicalRecord.objects.select_related('patient').all()
	return render(request, "clinical_records/clinicalrecord_list.html", {"records": records})

@login_required
def clinicalrecord_detail(request, pk):
	record = get_object_or_404(ClinicalRecord, pk=pk)
	return render(request, "clinical_records/clinicalrecord_detail.html", {"record": record})

@login_required
def clinicalrecord_create(request):
	if request.method == "POST":
		form = ClinicalRecordForm(request.POST)
		if form.is_valid():
			record = form.save()
			return redirect(reverse("clinicalrecord_detail", args=[record.pk]))
	else:
		form = ClinicalRecordForm()
	return render(request, "clinical_records/clinicalrecord_form.html", {"form": form})
