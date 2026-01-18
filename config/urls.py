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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from analytics.views import (
    analytics_dashboard,
    appointment_analytics,
    executive_summary,
    patient_analytics,
    revenue_analytics,
    user_activity_analytics,
)
from admin_dashboard.views import (
    department_overview,
    department_detail,
)
from appointments.views import (
    appointment_create,
    appointment_delete,
    appointment_detail,
    appointment_edit,
    appointment_list,
)
from audit_logs.views import audit_log_list
from billing.checkout_views import create_checkout_session, create_portal_session
from billing.upgrade_views import upgrade_plan, upgrade_success, upgrade_cancel
from billing.views import billing_dashboard
from billing.webhook_views import stripe_webhook
from billing.patient_billing_views import (
    patient_billing,
    patient_invoice_detail,
    patient_invoice_create,
    patient_invoice_mark_paid,
)
from clinical_records.ai_note_views import ai_note
from clinical_records.clinic_note_views import clinic_note_create
from clinical_records.notes_views import notes_dashboard
from clinical_records.views import (
    clinicalrecord_archive,
    clinicalrecord_create,
    clinicalrecord_detail,
    clinicalrecord_edit,
    clinicalrecord_list,
)
from documents.views import document_detail, upload_document
from fhir.info_views import fhir_info
from fhir.views import patient_read
from labs.views import (
    labresult_create,
    labresult_delete,
    labresult_detail,
    labresult_edit,
    labresult_list,
)
from patients.views import (
    patient_create,
    patient_delete,
    patient_detail,
    patient_edit,
    patient_list,
)
from referrals.views import create_referral, referral_list
from tenants.views import create_tenant, tenant_onboarding, view_plans
from users.admin_approval_views import approve_user, pending_users
from users.views import (
    TenantLoginView,
    TenantPasswordResetCompleteView,
    TenantPasswordResetConfirmView,
    TenantPasswordResetDoneView,
    TenantPasswordResetView,
    profile,
    register,
)


def landing(request):
    return render(request, "landing.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", dashboard, name="dashboard"),
    # Admin dashboard - departments
    path("admin/departments/", department_overview, name="department_overview"),
    path("admin/departments/<int:clinic_id>/", department_detail, name="department_detail"),
    # Custom admin views should precede the default admin include so they are not shadowed
    path("admin/pending-users/", pending_users, name="pending_users"),
    path("admin/approve-user/<int:user_id>/", approve_user, name="approve_user"),
    path("admin/", admin.site.urls),
    path("accounts/login/", TenantLoginView.as_view(), name="login"),
    path("accounts/register/", register, name="register"),
    path(
        "accounts/password-reset/",
        TenantPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        TenantPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        TenantPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password-reset/complete/",
        TenantPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("users/profile/", profile, name="user_profile"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("patients/", patient_list, name="patient_list"),
    path("patients/add/", patient_create, name="patient_create"),
    path("patients/<int:pk>/", patient_detail, name="patient_detail"),
    path("patients/<int:pk>/edit/", patient_edit, name="patient_edit"),
    path("patients/<int:pk>/delete/", patient_delete, name="patient_delete"),
    path("patients/<int:patient_pk>/billing/", patient_billing, name="patient_billing"),
    path("patients/<int:patient_pk>/billing/invoice/add/", patient_invoice_create, name="patient_invoice_create"),
    path("patients/billing/invoice/<int:invoice_pk>/", patient_invoice_detail, name="patient_invoice_detail"),
    path("patients/billing/invoice/<int:invoice_pk>/mark-paid/", patient_invoice_mark_paid, name="patient_invoice_mark_paid"),
    path("appointments/", appointment_list, name="appointment_list"),
    path("appointments/add/", appointment_create, name="appointment_create"),
    path("appointments/<int:pk>/", appointment_detail, name="appointment_detail"),
    path("appointments/<int:pk>/edit/", appointment_edit, name="appointment_edit"),
    path(
        "appointments/<int:pk>/delete/", appointment_delete, name="appointment_delete"
    ),
    path("clinical-records/", clinicalrecord_list, name="clinicalrecord_list"),
    path("clinical-records/notes/", notes_dashboard, name="notes_dashboard"),
    path("clinical-records/add/", clinicalrecord_create, name="clinicalrecord_create"),
    path(
        "clinical-records/<int:pk>/",
        clinicalrecord_detail,
        name="clinicalrecord_detail",
    ),
    path(
        "clinical-records/<int:pk>/edit/",
        clinicalrecord_edit,
        name="clinicalrecord_edit",
    ),
    path(
        "clinical-records/<int:pk>/archive/",
        clinicalrecord_archive,
        name="clinicalrecord_archive",
    ),
    path("clinical-records/ai-note/", ai_note, name="ai_note"),
    path(
        "clinical-records/clinic-note/create/",
        clinic_note_create,
        name="clinic_note_create",
    ),
    path("labs/", labresult_list, name="labresult_list"),
    path("labs/add/", labresult_create, name="labresult_create"),
    path("labs/<int:pk>/", labresult_detail, name="labresult_detail"),
    path("labs/<int:pk>/edit/", labresult_edit, name="labresult_edit"),
    path("labs/<int:pk>/delete/", labresult_delete, name="labresult_delete"),
    path("billing/", billing_dashboard, name="billing_dashboard"),
    path("audit_logs/", audit_log_list, name="audit_log_list"),
    path("referrals/", referral_list, name="referral_list"),
    path("referrals/create/", create_referral, name="create_referral"),
    path("documents/<int:pk>/", document_detail, name="document_detail"),
    path("documents/upload/", upload_document, name="upload_document"),
    # Analytics routes (Professional & Enterprise only)
    path("analytics/", analytics_dashboard, name="analytics_dashboard"),
    path("analytics/dashboard/", analytics_dashboard, name="analytics_dashboard_alt"),
    path("analytics/patients/", patient_analytics, name="patient_analytics"),
    path(
        "analytics/appointments/", appointment_analytics, name="appointment_analytics"
    ),
    path("analytics/revenue/", revenue_analytics, name="revenue_analytics"),
    path("analytics/users/", user_activity_analytics, name="user_activity_analytics"),
    path("analytics/executive/", executive_summary, name="executive_summary"),
    path("fhir/Patient/<int:pk>/", patient_read, name="fhir_patient_read"),
    path("fhir/", fhir_info, name="fhir_info"),
    # Add to urlpatterns:
    path("register-organization/", create_tenant, name="create_tenant"),
    path(
        "organizations/<int:tenant_id>/onboarding/",
        tenant_onboarding,
        name="tenant_onboarding",
    ),
    path("billing/plans/", view_plans, name="view_plans"),
    path("billing/upgrade/<str:plan>/", upgrade_plan, name="upgrade_plan"),
    path("billing/upgrade-success/", upgrade_success, name="upgrade_success"),
    path("billing/upgrade-cancel/", upgrade_cancel, name="upgrade_cancel"),
    path(
        "billing/create-checkout-session/",
        create_checkout_session,
        name="create_checkout_session",
    ),
    path(
        "billing/create-portal-session/",
        create_portal_session,
        name="create_portal_session",
    ),
    path("billing/webhook/", stripe_webhook, name="stripe_webhook"),
    # API v1 endpoints
    path("api/v1/", include("api.v1.urls")),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Google site verification
    path(
        "google421d5e7d96244ebd.html",
        lambda request: render(request, "google421d5e7d96244ebd.html"),
        name="google_site_verification",
    ),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)