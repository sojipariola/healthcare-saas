"""
API Serializers for Patient management
"""
from rest_framework import serializers
from .models import Patient, PatientNote


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model"""
    
    class Meta:
        model = Patient
        fields = [
            'id', 'patient_id', 'first_name', 'last_name', 'date_of_birth',
            'gender', 'email', 'phone', 'address', 'city', 'state', 'zip_code',
            'blood_type', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['patient_id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate patient data"""
        if 'date_of_birth' in data:
            from datetime import date
            if data['date_of_birth'] > date.today():
                raise serializers.ValidationError("Date of birth cannot be in the future")
        return data


class PatientDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer including sensitive information"""
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['patient_id', 'created_at', 'updated_at']


class PatientNoteSerializer(serializers.ModelSerializer):
    """Serializer for Patient notes"""
    
    class Meta:
        model = PatientNote
        fields = ['id', 'patient', 'title', 'content', 'note_type', 'created_by', 'created_at']
        read_only_fields = ['created_at', 'updated_at']
