"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from referrals.views import referral_list, create_referral
from django.contrib import admin

from django.urls import path
from billing.views import billing_dashboard
from audit_logs.views import audit_log_list
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from users.views import TenantLoginView, register, TenantPasswordResetView, TenantPasswordResetDoneView, TenantPasswordResetConfirmView, TenantPasswordResetCompleteView
from users.views import profile
from users.admin_approval_views import pending_users, approve_user

from patients.views import patient_list, patient_detail, patient_create, patient_edit, patient_delete
from appointments.views import appointment_list, appointment_detail, appointment_create, appointment_edit, appointment_delete
from clinical_records.views import clinicalrecord_list, clinicalrecord_detail, clinicalrecord_create, clinicalrecord_edit, clinicalrecord_archive
from clinical_records.ai_note_views import ai_note
from clinical_records.clinic_note_views import clinic_note_create
from labs.views import labresult_list, labresult_detail, labresult_create, labresult_edit, labresult_delete
from documents.views import upload_document
from analytics.views import analytics_dashboard
from fhir.views import patient_read

def landing(request):
    return render(request, "landing.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admin/", admin.site.urls),
    path("admin/pending-users/", pending_users, name="pending_users"),
    path("admin/approve-user/<int:user_id>/", approve_user, name="approve_user"),
    
    path("accounts/login/", TenantLoginView.as_view(), name="login"),
    path("accounts/register/", register, name="register"),
    path("accounts/password-reset/", TenantPasswordResetView.as_view(), name="password_reset"),
    path("accounts/password-reset/done/", TenantPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", TenantPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/password-reset/complete/", TenantPasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path("users/profile/", profile, name="user_profile"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path("patients/", patient_list, name="patient_list"),
    path("patients/add/", patient_create, name="patient_create"),
    path("patients/<int:pk>/", patient_detail, name="patient_detail"),
    path("patients/<int:pk>/edit/", patient_edit, name="patient_edit"),
    path("patients/<int:pk>/delete/", patient_delete, name="patient_delete"),
    
    path("appointments/", appointment_list, name="appointment_list"),
    path("appointments/add/", appointment_create, name="appointment_create"),
    path("appointments/<int:pk>/", appointment_detail, name="appointment_detail"),
    path("appointments/<int:pk>/edit/", appointment_edit, name="appointment_edit"),
    path("appointments/<int:pk>/delete/", appointment_delete, name="appointment_delete"),
    
    path("clinical-records/", clinicalrecord_list, name="clinicalrecord_list"),
    path("clinical-records/add/", clinicalrecord_create, name="clinicalrecord_create"),
    path("clinical-records/<int:pk>/", clinicalrecord_detail, name="clinicalrecord_detail"),
    path("clinical-records/<int:pk>/edit/", clinicalrecord_edit, name="clinicalrecord_edit"),
    path("clinical-records/<int:pk>/archive/", clinicalrecord_archive, name="clinicalrecord_archive"),
    path("clinical-records/ai-note/", ai_note, name="ai_note"),
    path("clinical-records/clinic-note/create/", clinic_note_create, name="clinic_note_create"),
    
    path("labs/", labresult_list, name="labresult_list"),
    path("labs/add/", labresult_create, name="labresult_create"),
    path("labs/<int:pk>/", labresult_detail, name="labresult_detail"),
    path("labs/<int:pk>/edit/", labresult_edit, name="labresult_edit"),
    path("labs/<int:pk>/delete/", labresult_delete, name="labresult_delete"),
    
    path("billing/", billing_dashboard, name="billing_dashboard"),
    path("audit_logs/", audit_log_list, name="audit_log_list"),
    path("referrals/", referral_list, name="referral_list"),
    path("referrals/create/", create_referral, name="create_referral"),
    path("documents/upload/", upload_document, name="upload_document"),
    path("analytics/dashboard/", analytics_dashboard, name="analytics_dashboard"),
    path("fhir/Patient/<int:pk>/", patient_read, name="fhir_patient_read"),
]
