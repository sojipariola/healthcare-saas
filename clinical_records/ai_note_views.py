from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from referrals.models import CLINIC_TYPES
from ai.note_taking import generate_clinical_note

@login_required
def ai_note(request):
    ai_note = None
    transcript = ''
    clinic_type = ''
    if request.method == "POST":
        transcript = request.POST.get("transcript", "")
        clinic_type = request.POST.get("clinic_type", "")
        if transcript and clinic_type:
            ai_note = generate_clinical_note(transcript, clinic_type)
    return render(request, "clinical_records/ai_note.html", {
        "ai_note": ai_note,
        "transcript": transcript,
        "clinic_type": clinic_type,
        "clinic_types": CLINIC_TYPES,
    })
