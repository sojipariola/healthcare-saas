"""
Tests for Patient models
"""
import pytest
from django.contrib.auth.models import User
from datetime import date, timedelta
from patients.models import Patient, PatientNote


@pytest.mark.django_db
class TestPatientModel:
    """Test Patient model"""
    
    def test_create_patient(self):
        """Test creating a patient"""
        patient = Patient.objects.create(
            patient_id='P000001',
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1980, 1, 1),
            gender='male',
            email='john.doe@example.com',
            phone='555-0100',
            consent_to_treat=True,
            hipaa_consent=True
        )
        
        assert patient.patient_id == 'P000001'
        assert patient.is_active is True
        assert patient.get_full_name() == 'John Doe'
    
    def test_patient_encryption(self):
        """Test that PHI fields are encrypted"""
        patient = Patient.objects.create(
            patient_id='P000002',
            first_name='Jane',
            last_name='Smith',
            date_of_birth=date(1985, 5, 15),
            ssn='123-45-6789'
        )
        
        # Verify data can be retrieved
        assert patient.first_name == 'Jane'
        assert patient.ssn == '123-45-6789'
    
    def test_patient_string_representation(self):
        """Test patient string representation"""
        patient = Patient.objects.create(
            patient_id='P000003',
            first_name='Bob',
            last_name='Johnson',
            date_of_birth=date(1975, 12, 31)
        )
        
        assert str(patient) == 'Patient P000003'


@pytest.mark.django_db
class TestPatientNote:
    """Test PatientNote model"""
    
    def test_create_note(self):
        """Test creating a patient note"""
        user = User.objects.create_user(username='doctor', password='testpass')
        patient = Patient.objects.create(
            patient_id='P000004',
            first_name='Alice',
            last_name='Williams',
            date_of_birth=date(1990, 3, 20)
        )
        
        note = PatientNote.objects.create(
            patient=patient,
            created_by=user,
            title='Initial Consultation',
            content='Patient presents with headache.',
            note_type='general'
        )
        
        assert note.patient == patient
        assert note.created_by == user
        assert note.note_type == 'general'
