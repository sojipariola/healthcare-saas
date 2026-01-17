"""
API Views for Patient management with RBAC
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Patient, PatientNote
from .serializers import PatientSerializer, PatientDetailSerializer, PatientNoteSerializer
from audit_logs.models import DataAccessLog


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient CRUD operations with audit logging
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_active', 'gender', 'primary_physician']
    search_fields = ['patient_id', 'first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'patient_id']
    
    def get_serializer_class(self):
        """Use detailed serializer for retrieve actions"""
        if self.action == 'retrieve':
            return PatientDetailSerializer
        return PatientSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Log PHI access when viewing patient details"""
        instance = self.get_object()
        
        # Create audit log for PHI access
        DataAccessLog.objects.create(
            user=request.user,
            patient_id=instance.patient_id,
            access_type='view_demographics',
            access_reason=request.query_params.get('reason', 'Patient record review')
        )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def medical_history(self, request, pk=None):
        """Get patient medical history"""
        patient = self.get_object()
        
        # Log access
        DataAccessLog.objects.create(
            user=request.user,
            patient_id=patient.patient_id,
            access_type='view_medical_history',
            access_reason=request.query_params.get('reason', 'Medical history review')
        )
        
        return Response({
            'allergies': patient.allergies,
            'current_medications': patient.current_medications,
            'medical_history': patient.medical_history,
            'blood_type': patient.blood_type
        })


class PatientNoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient notes
    """
    queryset = PatientNote.objects.all()
    serializer_class = PatientNoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'note_type', 'created_by']
    
    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)
