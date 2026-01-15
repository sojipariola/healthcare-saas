from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import LabResult
from patients.models import Patient
from .forms import LabResultForm
from django.contrib.auth.decorators import login_required, permission_required




@login_required
@permission_required('labs.change_labresult', raise_exception=True)
def labresult_edit(request, pk):
	result = get_object_or_404(LabResult, pk=pk)
	if request.method == "POST":
		form = LabResultForm(request.POST, instance=result)
		if form.is_valid():
			form.save()
			return redirect(reverse("labresult_detail", args=[result.pk]))
	else:
		form = LabResultForm(instance=result)
	return render(request, "labs/labresult_form.html", {"form": form, "edit": True})

@login_required
@permission_required('labs.delete_labresult', raise_exception=True)
def labresult_delete(request, pk):
	result = get_object_or_404(LabResult, pk=pk)
	if request.method == "POST":
		result.delete()
		return redirect(reverse("labresult_list"))
	return render(request, "labs/labresult_confirm_delete.html", {"result": result})


@login_required
def labresult_list(request):
	results = LabResult.objects.select_related('patient').all()
	return render(request, "labs/labresult_list.html", {"results": results})

@login_required
def labresult_detail(request, pk):
	result = get_object_or_404(LabResult, pk=pk)
	return render(request, "labs/labresult_detail.html", {"result": result})

@login_required
def labresult_create(request):
	if request.method == "POST":
		form = LabResultForm(request.POST)
		if form.is_valid():
			result = form.save()
			return redirect(reverse("labresult_detail", args=[result.pk]))
	else:
		form = LabResultForm()
	return render(request, "labs/labresult_form.html", {"form": form})
