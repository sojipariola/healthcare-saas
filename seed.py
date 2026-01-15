from django.core.management import execute_from_command_line
import os
import django
import random
from datetime import datetime, timedelta
from tenants.models import Tenant
from users.models import CustomUser
from patients.models import Patient
from appointments.models import Appointment
from clinical_records.models import ClinicalRecord
from labs.models import LabResult
from django.contrib.auth.hashers import make_password
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()



# Tenants
tenant1 = Tenant.objects.create(name="Alpha Clinic", subdomain="alpha")
tenant2 = Tenant.objects.create(name="Beta Health", subdomain="beta")

# Users
user1 = CustomUser.objects.create(username="admin1", email="admin1@alpha.com", tenant=tenant1, role="admin", password=make_password("password"))
user2 = CustomUser.objects.create(username="user2", email="user2@beta.com", tenant=tenant2, role="user", password=make_password("password"))

# Patients
patients = []
for i in range(1, 6):
    p = Patient.objects.create(
        first_name=f"John{i}",
        last_name=f"Doe{i}",
        date_of_birth=datetime(1980+i, 1, 1).date(),
        email=f"john{i}@example.com",
        phone=f"555-000{i}"
    )
    patients.append(p)

# Appointments
for i, patient in enumerate(patients):
    Appointment.objects.create(
        patient=patient,
        scheduled_for=datetime.now() + timedelta(days=i),
        status="scheduled"
    )

# Clinical Records
for patient in patients:
    ClinicalRecord.objects.create(
        patient=patient,
        note=f"Initial consultation for {patient.first_name} {patient.last_name}."
    )

# Lab Results
for patient in patients:
    LabResult.objects.create(
        patient=patient,
        result=f"Lab result for {patient.first_name} {patient.last_name}: Normal."
    )

print("Database seeded successfully.")
