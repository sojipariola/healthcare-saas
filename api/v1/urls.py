"""
API URL routing with DRF routers
"""

from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, AppointmentViewSet, ClinicalRecordViewSet,
    LabResultViewSet, DashboardViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'clinical-records', ClinicalRecordViewSet, basename='clinical-record')
router.register(r'lab-results', LabResultViewSet, basename='lab-result')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls
