"""
API Serializers for core models
Handles PHI-aware serialization and validation
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from patients.models import Patient
from appointments.models import Appointment
from clinical_records.models import ClinicalRecord
from labs.models import LabResult
from users.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User/Staff member serializer"""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active']
        read_only_fields = ['id', 'email']


class PatientSerializer(serializers.ModelSerializer):
    """Patient serializer with PHI considerations"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'date_of_birth', 'gender', 
            'email', 'phone', 'address', 'city', 'state', 
            'zip_code', 'insurance_provider', 'insurance_id',
            'medical_record_number', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment serializer"""
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    provider_name = serializers.CharField(source='provider.get_full_name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'provider', 'provider_name',
            'appointment_date', 'appointment_time', 'duration_minutes',
            'appointment_type', 'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClinicalRecordSerializer(serializers.ModelSerializer):
    """Clinical Record (SOAP notes) serializer"""
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    provider_name = serializers.CharField(source='provider.get_full_name', read_only=True)
    
    class Meta:
        model = ClinicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'provider', 'provider_name',
            'visit_date', 'subjective', 'objective', 'assessment', 'plan',
            'is_locked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LabResultSerializer(serializers.ModelSerializer):
    """Lab Result serializer"""
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    
    class Meta:
        model = LabResult
        fields = [
            'id', 'patient', 'patient_name', 'test_name', 'test_code',
            'result_value', 'result_unit', 'reference_range', 'status',
            'lab_date', 'result_date', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DashboardStatsSerializer(serializers.Serializer):
    """Dashboard statistics serializer"""
    total_patients = serializers.IntegerField()
    appointments_today = serializers.IntegerField()
    pending_appointments = serializers.IntegerField()
    new_patients_this_month = serializers.IntegerField()
    active_users = serializers.IntegerField()
