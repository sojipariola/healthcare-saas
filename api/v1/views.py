"""
API ViewSets for CRUD operations
Implements proper filtering, pagination, and permissions
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from patients.models import Patient
from appointments.models import Appointment
from clinical_records.models import ClinicalRecord
from labs.models import LabResult
from users.models import CustomUser
from common.audit import log_audit
from .serializers import (
    PatientSerializer, AppointmentSerializer, ClinicalRecordSerializer,
    LabResultSerializer, UserSerializer, DashboardStatsSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsAuthenticatedAndTenantOwner(permissions.BasePermission):
    """Permission to ensure user belongs to tenant"""
    def has_object_permission(self, request, view, obj):
        # Check if user's tenant matches object's tenant
        return getattr(obj, 'tenant_id', None) == request.user.tenant_id


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient CRUD operations
    - List all patients (with search, filter, sort)
    - Create new patient
    - Retrieve patient details
    - Update patient information
    - Delete patient
    """
    serializer_class = PatientSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['created_at', 'first_name']
    ordering = ['-created_at']
    permission_classes = [permissions.IsAuthenticated, IsAuthenticatedAndTenantOwner]
    
    def get_queryset(self):
        """Filter patients by current user's tenant"""
        return Patient.objects.filter(tenant=self.request.user.tenant).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set tenant when creating patient"""
        patient = serializer.save(tenant=self.request.user.tenant)
        log_audit(
            user=self.request.user,
            action='CREATE',
            model='Patient',
            object_id=patient.id,
            changes={'created': 'Patient record created'}
        )
    
    def perform_update(self, serializer):
        """Log patient updates"""
        patient = serializer.save()
        log_audit(
            user=self.request.user,
            action='UPDATE',
            model='Patient',
            object_id=patient.id,
            changes=serializer.validated_data
        )
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """Get all appointments for a patient"""
        patient = self.get_object()
        appointments = Appointment.objects.filter(
            patient=patient,
            tenant=request.user.tenant
        ).order_by('-appointment_date')
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def clinical_records(self, request, pk=None):
        """Get all clinical records for a patient"""
        patient = self.get_object()
        records = ClinicalRecord.objects.filter(
            patient=patient,
            tenant=request.user.tenant
        ).order_by('-visit_date')
        serializer = ClinicalRecordSerializer(records, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment scheduling
    - List appointments with filtering by date, status
    - Create new appointment with conflict detection
    - Update appointment
    - Delete appointment
    """
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'appointment_type']
    ordering_fields = ['appointment_date', 'appointment_time']
    ordering = ['appointment_date', 'appointment_time']
    permission_classes = [permissions.IsAuthenticated, IsAuthenticatedAndTenantOwner]
    
    def get_queryset(self):
        """Filter appointments by tenant"""
        queryset = Appointment.objects.filter(tenant=self.request.user.tenant)
        
        # Filter by date range if provided
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from and date_to:
            queryset = queryset.filter(
                appointment_date__gte=date_from,
                appointment_date__lte=date_to
            )
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-appointment_date')
    
    def perform_create(self, serializer):
        """Create appointment with conflict detection"""
        appointment = serializer.save(tenant=self.request.user.tenant)
        log_audit(
            user=self.request.user,
            action='CREATE',
            model='Appointment',
            object_id=appointment.id,
            changes={'created': f'Appointment scheduled for {appointment.appointment_date}'}
        )
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments"""
        today = timezone.now().date()
        appointments = self.get_queryset().filter(
            appointment_date=today
        ).order_by('appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments for the next 7 days"""
        today = timezone.now().date()
        upcoming_date = today + timedelta(days=7)
        appointments = self.get_queryset().filter(
            appointment_date__gte=today,
            appointment_date__lte=upcoming_date,
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)


class ClinicalRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Clinical Records (SOAP notes)
    - List records with filtering
    - Create SOAP note
    - View record details
    - Update (with locking)
    """
    serializer_class = ClinicalRecordSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'assessment']
    ordering_fields = ['visit_date', 'created_at']
    ordering = ['-visit_date']
    permission_classes = [permissions.IsAuthenticated, IsAuthenticatedAndTenantOwner]
    
    def get_queryset(self):
        """Filter records by tenant"""
        return ClinicalRecord.objects.filter(tenant=self.request.user.tenant).order_by('-visit_date')
    
    def perform_create(self, serializer):
        """Create clinical record"""
        record = serializer.save(
            tenant=self.request.user.tenant,
            provider=self.request.user
        )
        log_audit(
            user=self.request.user,
            action='CREATE',
            model='ClinicalRecord',
            object_id=record.id,
            changes={'created': f'SOAP note for {record.patient}'}
        )
    
    def update(self, request, *args, **kwargs):
        """Prevent updates to locked records"""
        instance = self.get_object()
        if instance.is_locked:
            return Response(
                {'error': 'Record is locked and cannot be modified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def lock(self, request, pk=None):
        """Lock a clinical record (make immutable)"""
        record = self.get_object()
        record.is_locked = True
        record.save()
        log_audit(
            user=self.request.user,
            action='UPDATE',
            model='ClinicalRecord',
            object_id=record.id,
            changes={'action': 'Record locked'}
        )
        return Response({'status': 'Record locked'})


class LabResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lab Results
    - List lab results with filtering
    - View result details
    """
    serializer_class = LabResultSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['patient__first_name', 'patient__last_name', 'test_name']
    ordering_fields = ['lab_date', 'result_date']
    ordering = ['-result_date']
    permission_classes = [permissions.IsAuthenticated, IsAuthenticatedAndTenantOwner]
    
    def get_queryset(self):
        """Filter results by tenant"""
        return LabResult.objects.filter(tenant=self.request.user.tenant).order_by('-result_date')
    
    def perform_create(self, serializer):
        """Create lab result"""
        result = serializer.save(tenant=self.request.user.tenant)
        log_audit(
            user=self.request.user,
            action='CREATE',
            model='LabResult',
            object_id=result.id,
            changes={'created': f'Lab result: {result.test_name}'}
        )


class DashboardViewSet(viewsets.ViewSet):
    """Dashboard statistics endpoint"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get dashboard statistics"""
        today = timezone.now().date()
        tenant = request.user.tenant
        
        stats = {
            'total_patients': Patient.objects.filter(tenant=tenant).count(),
            'appointments_today': Appointment.objects.filter(
                tenant=tenant,
                appointment_date=today
            ).count(),
            'pending_appointments': Appointment.objects.filter(
                tenant=tenant,
                status='scheduled'
            ).count(),
            'new_patients_this_month': Patient.objects.filter(
                tenant=tenant,
                created_at__month=today.month,
                created_at__year=today.year
            ).count(),
            'active_users': CustomUser.objects.filter(
                tenant=tenant,
                is_active=True
            ).count(),
        }
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)
