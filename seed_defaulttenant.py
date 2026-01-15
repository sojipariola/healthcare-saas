from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tenants.models import Tenant
from patients.models import Patient
from appointments.models import Appointment
from clinical_records.models import ClinicalRecord
from labs.models import LabResult
from billing.models import Subscription, Payment
from users.roles import assign_role
from appointments.models import Availability

class Command(BaseCommand):
    help = 'Seed all tables for DefaultTenant'

    def handle(self, *args, **options):
        User = get_user_model()
        tenant, _ = Tenant.objects.get_or_create(name='DefaultTenant', subdomain='default')

        # Create users
        admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass', tenant=tenant)
        user = User.objects.create_user(username='user1', email='user1@example.com', password='userpass', tenant=tenant)

        # Create patients
        p1 = Patient.objects.create(name='John Doe', tenant=tenant)
        p2 = Patient.objects.create(name='Jane Smith', tenant=tenant)

        # Create appointments
        Appointment.objects.create(patient=p1, tenant=tenant, date='2026-01-15', reason='Checkup')
        Appointment.objects.create(patient=p2, tenant=tenant, date='2026-01-16', reason='Consultation')

        # Create clinical records
        ClinicalRecord.objects.create(patient=p1, tenant=tenant, notes='Healthy', locked=False)
        ClinicalRecord.objects.create(patient=p2, tenant=tenant, notes='Needs follow-up', locked=False)

        # Create lab results
        LabResult.objects.create(patient=p1, tenant=tenant, result='Normal', date='2026-01-15')
        LabResult.objects.create(patient=p2, tenant=tenant, result='High cholesterol', date='2026-01-16')

        # Create subscriptions and payments
        sub = Subscription.objects.create(tenant=tenant, plan='Pro', active=True)
        Payment.objects.create(subscription=sub, amount=99.99, date='2026-01-10', status='Completed')

        self.stdout.write(self.style.SUCCESS('Seeded all tables for DefaultTenant'))




        # Assign doctor role to user1 and create their availability

        assign_role(user, 'doctor')

        # Create availability slots for the doctor
        Availability.objects.create(user=user, tenant=tenant, date='2026-01-15', start_time='09:00', end_time='12:00')
        Availability.objects.create(user=user, tenant=tenant, date='2026-01-16', start_time='13:00', end_time='16:00')

        # Create appointments for patients with the available doctor
        Appointment.objects.create( patient=p1, tenant=tenant, date='2026-01-15', reason='Checkup', doctor=user, time='09:30' )
        Appointment.objects.create( patient=p2, tenant=tenant, date='2026-01-16', reason='Consultation', doctor=user, time='13:30' )
        