from django.contrib import admin
from .models import Clinic, Referral

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("name", "clinic_type", "tenant")
    list_filter = ("clinic_type", "tenant")
    search_fields = ("name",)

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("patient", "from_clinic", "to_clinic", "referred_by", "created_at", "accepted")
    list_filter = ("from_clinic", "to_clinic", "accepted")
    search_fields = ("patient__name", "from_clinic__name", "to_clinic__name")
