import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

import random
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from analytics.models import AnalyticsEvent
from appointments.models import Appointment
from audit_logs.models import AuditLog
from billing.models import Payment, SubscriptionPlan, TenantSubscription
from clinical_records.models import ClinicalRecord
from documents.models import Document
from labs.models import LabResult
from patients.models import Patient
from referrals.models import CLINIC_TYPES, Clinic, Referral
from tenants.models import Tenant


User = get_user_model()

print("=" * 60)
print("🚀 Healthcare SaaS Database Seeding Script")
print("=" * 60)

print("\n🔄 Creating default tenant...")
tenant, created = Tenant.objects.get_or_create(
    name="DefaultTenant",
    subdomain="default",
    defaults={
        "plan": "free_trial",
        "trial_started_at": timezone.now(),
        "trial_ended_at": timezone.now() + timedelta(days=14),
        "is_active": True,
    },
)
print(f"✓ Tenant: {tenant.name} (created={created})")

print("\n👤 Creating users...")
admin, created = User.objects.get_or_create(
    username="admin",
    defaults={
        "email": "admin@example.com",
        "tenant": tenant,
        "is_staff": True,
        "is_superuser": True,
    },
)
if created:
    admin.set_password("adminpass")
    admin.save()
print(f"✓ Admin user: {admin.username}")

user1, created = User.objects.get_or_create(
    username="user1",
    defaults={
        "email": "user1@example.com",
        "tenant": tenant,
        "is_staff": False,
    },
)
if created:
    user1.set_password("userpass")
    user1.save()
print(f"✓ User: {user1.username}")

user2, created = User.objects.get_or_create(
    username="doctor1",
    defaults={
        "email": "doctor1@example.com",
        "tenant": tenant,
        "is_staff": False,
    },
)
if created:
    user2.set_password("docpass")
    user2.save()
print(f"✓ Doctor user: {user2.username}")

print("\n👥 Creating patients...")
patients = []
patient_data = [
    ("John", "Doe", "1990-05-15", "john@example.com", "555-0001"),
    ("Jane", "Smith", "1985-08-20", "jane@example.com", "555-0002"),
    ("Robert", "Johnson", "1992-03-10", "robert@example.com", "555-0003"),
    ("Emily", "Williams", "1988-11-25", "emily@example.com", "555-0004"),
    ("Michael", "Brown", "1995-07-12", "michael@example.com", "555-0005"),
]

for first, last, dob, email, phone in patient_data:
    p, created = Patient.objects.get_or_create(
        first_name=first,
        last_name=last,
        tenant=tenant,
        defaults={
            "date_of_birth": datetime.strptime(dob, "%Y-%m-%d").date(),
            "email": email,
            "phone": phone,
        },
    )
    patients.append(p)
    print(f"✓ Patient: {p.first_name} {p.last_name}")

print("\n📅 Creating appointments...")
for i, patient in enumerate(patients):
    for j in range(random.randint(1, 3)):
        appt, created = Appointment.objects.get_or_create(
            patient=patient,
            tenant=tenant,
            scheduled_for=timezone.now() + timedelta(days=random.randint(1, 30)),
            defaults={
                "status": random.choice(["scheduled", "completed", "cancelled"]),
            },
        )
        if created:
            print(
                f"✓ Appointment for {patient.first_name} - {appt.scheduled_for.strftime('%Y-%m-%d')}"
            )

print("\n📝 Creating clinical records...")
soap_notes = [
    "Patient presents with general checkup. Vitals stable. No complaints.",
    "Follow-up visit. All vitals normal. Continue current treatment plan.",
    "Patient reports mild headaches. Prescribed analgesics. Follow up in 1 week.",
    "Lab results normal. Patient doing well. Maintain current lifestyle.",
    "Initial consultation. Comprehensive evaluation completed. Referred to specialist.",
]

for patient in patients:
    for i in range(random.randint(1, 3)):
        cr, created = ClinicalRecord.objects.get_or_create(
            patient=patient,
            tenant=tenant,
            defaults={
                "note": random.choice(soap_notes),
            },
        )
        if created:
            print(f"✓ Clinical record for {patient.first_name}")

print("\n🧪 Creating lab results...")
lab_results_text = [
    "Blood Work - Normal. All values within range.",
    "Cholesterol Panel - High cholesterol detected. Recommend dietary changes.",
    "Glucose Test - Normal fasting glucose level.",
    "Complete Blood Count - All parameters normal.",
    "Thyroid Function - TSH levels normal.",
    "Kidney Function - Creatinine and BUN within normal range.",
    "Liver Function - AST and ALT levels normal.",
]

for patient in patients:
    for i in range(random.randint(1, 2)):
        lab = LabResult.objects.create(
            patient=patient,
            tenant=tenant,
            result=random.choice(lab_results_text),
        )
        print(f"✓ Lab result for {patient.first_name}")

print("\n🏥 Creating clinics for referrals...")
clinics = []
clinic_names = [
    "General Practice",
    "Cardiology Center",
    "Dermatology Clinic",
    "Orthopedic Center",
]
clinic_types = ["general_practice", "cardiology", "dermatology", "orthopedic"]

for name, clinic_type in zip(clinic_names, clinic_types):
    clinic, created = Clinic.objects.get_or_create(
        name=name,
        tenant=tenant,
        defaults={
            "clinic_type": clinic_type,
        },
    )
    clinics.append(clinic)
    print(f"✓ Clinic: {clinic.name}")

print("\n📤 Creating referrals...")
for patient in patients:
    for i in range(random.randint(0, 2)):
        if len(clinics) >= 2:
            from_clinic = random.choice(clinics)
            to_clinic = random.choice([c for c in clinics if c != from_clinic])
            ref, created = Referral.objects.get_or_create(
                patient=patient,
                from_clinic=from_clinic,
                to_clinic=to_clinic,
                defaults={
                    "referred_by": random.choice([admin, user1, user2]),
                    "notes": "Follow-up care and specialized treatment",
                    "accepted": random.choice([True, False]),
                },
            )
            if created:
                print(f"✓ Referral for {patient.first_name} from {from_clinic.name}")

print("\n💳 Creating subscription plans...")
plans_data = [
    ("Free Trial", 0, "trial", "14-day free trial"),
    ("Starter", 99.00, "monthly", "Up to 5 users, 100 patients"),
    ("Professional", 299.00, "monthly", "Up to 20 users, 500 patients"),
    ("Enterprise", 999.00, "monthly", "Unlimited users and patients"),
]

subscription_plans = {}
for name, price, interval, desc in plans_data:
    plan, created = SubscriptionPlan.objects.get_or_create(
        name=name,
        defaults={
            "price": price,
            "interval": interval,
            "description": desc,
            "is_active": True,
        },
    )
    subscription_plans[name] = plan
    print(f"✓ Plan: {plan.name} (${plan.price}/{interval})")

print("\n📋 Creating tenant subscriptions...")
current_plan = subscription_plans["Free Trial"]
sub, created = TenantSubscription.objects.get_or_create(
    tenant=tenant,
    plan=current_plan,
    defaults={
        "active": True,
        "start_date": timezone.now().date(),
        "end_date": (timezone.now() + timedelta(days=14)).date(),
    },
)
print(f"✓ Subscription: {tenant.name} -> {current_plan.name}")

print("\n💰 Creating payments...")
payment_reasons = [
    "Subscription Payment",
    "Trial Upgrade",
    "Monthly Billing",
    "Annual Billing",
]
for i in range(5):
    payment = Payment.objects.create(
        tenant=tenant,
        amount=random.choice([99.00, 299.00, 999.00]),
        currency="USD",
        description=random.choice(payment_reasons),
        is_subscription=True,
    )
    print(f"✓ Payment: ${payment.amount} - {payment.description}")

print("\n📄 Creating documents...")
document_types = [
    "Lab Report",
    "Prescription",
    "Medical Record",
    "Insurance Form",
    "Test Result",
]
for patient in patients:
    for i in range(random.randint(1, 2)):
        doc = Document.objects.create(
            patient=patient,
            uploaded_by=random.choice([admin, user1, user2]),
            description=f"{random.choice(document_types)} for {patient.first_name}",
        )
        print(f"✓ Document for {patient.first_name}")

print("\n📊 Creating analytics events...")
event_types = [
    "patient_created",
    "appointment_scheduled",
    "lab_result_added",
    "clinical_record_created",
    "report_generated",
    "user_login",
]

for i in range(20):
    event = AnalyticsEvent.objects.create(
        tenant=tenant,
        event_type=random.choice(event_types),
        user_id=random.choice([admin.id, user1.id, user2.id]),
        metadata={
            "source": "web",
            "platform": "django",
        },
    )
    print(f"✓ Analytics event: {event.event_type}")

print("\n📋 Creating audit logs...")
audit_actions = [
    ("user_registered", "User registered"),
    ("login_success", "User logged in"),
    ("user_approved", "User approved by admin"),
]

for i in range(20):
    action, details = random.choice(audit_actions)
    audit = AuditLog.objects.create(
        tenant=tenant,
        user=random.choice([admin, user1, user2]),
        action=action,
        details=details,
    )
    print(f"✓ Audit log: {audit.user.username} - {action}")

print("\n" + "=" * 60)
print("✅ DATABASE SEEDING COMPLETE!")
print("=" * 60)

print(f"\n📊 SUMMARY:")
print(f"  Tenant: {tenant.name}")
print(f"  Users: {User.objects.filter(tenant=tenant).count()}")
print(f"  Patients: {Patient.objects.filter(tenant=tenant).count()}")
print(f"  Appointments: {Appointment.objects.filter(tenant=tenant).count()}")
print(f"  Clinical Records: {ClinicalRecord.objects.filter(tenant=tenant).count()}")
print(f"  Lab Results: {LabResult.objects.filter(tenant=tenant).count()}")
print(f"  Clinics: {Clinic.objects.filter(tenant=tenant).count()}")
print(f"  Referrals: {Referral.objects.filter(from_clinic__tenant=tenant).count()}")
print(f"  Subscription Plans: {SubscriptionPlan.objects.count()}")
print(
    f"  Tenant Subscriptions: {TenantSubscription.objects.filter(tenant=tenant).count()}"
)
print(f"  Payments: {Payment.objects.filter(tenant=tenant).count()}")
print(f"  Documents: {Document.objects.filter(patient__tenant=tenant).count()}")
print(f"  Analytics Events: {AnalyticsEvent.objects.filter(tenant=tenant).count()}")
print(f"  Audit Logs: {AuditLog.objects.filter(tenant=tenant).count()}")

print("\n🔑 TEST CREDENTIALS:")
print("  Admin: admin / adminpass")
print("  User: user1 / userpass")
print("  Doctor: doctor1 / docpass")

print("\n🌐 ENDPOINTS:")
print("  Dashboard: http://localhost:8000/dashboard/")
print("  Patients: http://localhost:8000/patients/")
print("  Appointments: http://localhost:8000/appointments/")
print("  Billing: http://localhost:8000/billing/")
print("  Plans: http://localhost:8000/billing/plans/")
print("  FHIR: http://localhost:8000/fhir/")

print("\n" + "=" * 60)
