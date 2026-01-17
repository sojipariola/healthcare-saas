"""
URL configuration for healthcare_saas project - Multi-tenant Healthcare SaaS Platform
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from patients.views import PatientViewSet, PatientNoteViewSet

# API Router
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'patient-notes', PatientNoteViewSet, basename='patient-note')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    
    # Health check endpoint
    path('health/', lambda request: __import__('django.http').JsonResponse({'status': 'healthy'})),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Healthcare SaaS Administration"
admin.site.site_title = "Healthcare SaaS Admin"
admin.site.index_title = "Welcome to Healthcare SaaS Platform"
