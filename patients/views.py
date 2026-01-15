from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import PatientForm
from .models import Patient
from django.contrib.auth.decorators import permission_required, login_required

@login_required
@permission_required('patients.change_patient', raise_exception=True)
def patient_edit(request, pk):
	patient = get_object_or_404(Patient, pk=pk)
	if request.method == "POST":
		form = PatientForm(request.POST, instance=patient)
		if form.is_valid():
			form.save()
			return redirect(reverse("patient_detail", args=[patient.pk]))
	else:
		form = PatientForm(instance=patient)
	return render(request, "patients/patient_form.html", {"form": form, "edit": True})

@login_required
@permission_required('patients.delete_patient', raise_exception=True)
def patient_delete(request, pk):
	patient = get_object_or_404(Patient, pk=pk)
	if request.method == "POST":
		patient.delete()
		return redirect(reverse("patient_list"))
	return render(request, "patients/patient_confirm_delete.html", {"patient": patient})

@login_required
def patient_detail(request, pk):
	patient = get_object_or_404(Patient, pk=pk)
	return render(request, "patients/patient_detail.html", {"patient": patient})

@login_required
def patient_create(request):
	if request.method == "POST":
		form = PatientForm(request.POST)
		if form.is_valid():
			patient = form.save()
			return redirect(reverse("patient_detail", args=[patient.pk]))
	else:
		form = PatientForm()
	return render(request, "patients/patient_form.html", {"form": form})

@login_required
def patient_list(request):
	patients = Patient.objects.all()
	return render(request, "patients/patient_list.html", {"patients": patients})
