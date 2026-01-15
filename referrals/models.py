from django.db import models
from tenants.models import Tenant
from patients.models import Patient
from users.models import CustomUser

CLINIC_TYPES = [
    ("general_practice", "General Practice"),
    ("pediatrics", "Pediatrics"),
    ("dental", "Dental"),
    ("eye", "Eye Clinic"),
    ("womens_health", "Women’s Health"),
    ("dermatology", "Dermatology"),
    ("mental_health", "Mental Health"),
    ("physiotherapy", "Physiotherapy"),
    ("orthopedic", "Orthopedic"),
    ("cardiology", "Cardiology"),
    ("ent", "ENT"),
    ("urology", "Urology"),
    ("oncology", "Oncology"),
    ("allergy", "Allergy & Immunology"),
    ("pain", "Pain Management"),
    ("gastroenterology", "Gastroenterology"),
    ("endocrinology", "Endocrinology"),
    ("neurology", "Neurology"),
    ("surgical", "Surgical Specialty"),
    ("urgent_care", "Urgent Care"),
    ("multi_specialty", "Multi-specialty"),
    ("telemedicine", "Telemedicine"),
    ("community_health", "Community Health"),
    ("fertility", "Fertility & Reproductive Health"),
    ("geriatric", "Geriatric"),
]

class Clinic(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    clinic_type = models.CharField(max_length=32, choices=CLINIC_TYPES)

    def __str__(self):
        return f"{self.name} ({self.get_clinic_type_display()})"

class Referral(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    from_clinic = models.ForeignKey(Clinic, related_name='referrals_sent', on_delete=models.CASCADE)
    to_clinic = models.ForeignKey(Clinic, related_name='referrals_received', on_delete=models.CASCADE)
    referred_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Referral of {self.patient} from {self.from_clinic} to {self.to_clinic}"
