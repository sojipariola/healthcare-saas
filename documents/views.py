from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentUploadForm
from .models import Document
from patients.models import Patient
from referrals.models import Referral
from django.contrib import messages

@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, "Document uploaded successfully.")
            return redirect("upload_document")
    else:
        form = DocumentUploadForm()
    return render(request, "documents/upload.html", {"form": form})
