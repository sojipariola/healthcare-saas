from common.audit import log_audit
from .notifications import notify_admins_of_new_user

from django.contrib.auth import views as auth_views
from .registration_forms import TenantUserRegistrationForm
from billing.free_trial import is_tenant_in_free_trial, is_free_user_limit_reached, is_free_patient_limit_reached, send_trial_expiry_notification, free_trial_days_left
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import TenantAwareAuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging
# Set up logger
logger = logging.getLogger(__name__)

# Registration view
def register(request):
	if request.method == "POST":
		form = TenantUserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			tenant = user.tenant
			# Free trial logic
			if is_tenant_in_free_trial(tenant):
				if is_free_user_limit_reached(tenant):
					messages.error(request, "Free trial limit: max 2 users. Upgrade to add more.")
					return render(request, "registration/register.html", {"form": form})
				if is_free_patient_limit_reached(tenant):
					messages.error(request, "Free trial limit: max 5 patients. Upgrade to add more.")
					return render(request, "registration/register.html", {"form": form})
				notify_admins_of_new_user(user)
				log_audit("user_registered", user=user, tenant=tenant, details=f"User {user.username} registered for tenant {tenant}.")
				messages.success(request, f"Registration successful. {free_trial_days_left(tenant)} days left in free trial. Limits: 2 users, 5 patients. Admins notified.")
				return redirect("login")
			else:
				send_trial_expiry_notification(tenant)
				messages.error(request, "Free trial expired. Please upgrade your plan to continue using ClinicCloud.")
				return render(request, "registration/register.html", {"form": form})
		else:
			logger.error(f"Registration error: {form.errors.as_json()}")
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f"{field}: {error}")
	else:
		form = TenantUserRegistrationForm()
	return render(request, "registration/register.html", {"form": form})

# Password reset views (use Django's built-in views)
class TenantPasswordResetView(auth_views.PasswordResetView):
	template_name = "registration/password_reset_form.html"
	email_template_name = "registration/password_reset_email.html"
	subject_template_name = "registration/password_reset_subject.txt"
	success_url = "/accounts/password-reset/done/"
	def form_valid(self, form):
		messages.success(self.request, "If the email exists, a password reset link has been sent.")
		return super().form_valid(form)

class TenantPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = "registration/password_reset_done.html"

class TenantPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	template_name = "registration/password_reset_confirm.html"
	success_url = "/accounts/password-reset/complete/"
	def form_valid(self, form):
		messages.success(self.request, "Your password has been set. You may now log in.")
		return super().form_valid(form)

class TenantPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = "registration/password_reset_complete.html"



class TenantLoginView(LoginView):
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		next_url = self.request.GET.get('next') or self.request.POST.get('next')
		context['next'] = next_url or ''
		return context

	authentication_form = TenantAwareAuthenticationForm
	template_name = "registration/login.html"

	def form_valid(self, form):
		tenant = form.cleaned_data.get("tenant_obj")
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(self.request, username=username, password=password, tenant=tenant)
		if user is not None:
			login(self.request, user)
			next_url = self.request.GET.get('next') or self.request.POST.get('next')
			if next_url:
				return redirect(next_url)
			return redirect('dashboard')
		else:
			logger.error(f"Login error for user '{username}' and tenant '{tenant}': Invalid credentials or tenant.")
			messages.error(self.request, "Invalid login credentials or tenant.")
			return self.form_invalid(form)

@login_required
def profile(request):
    return render(request, "users/profile.html", {"user": request.user})



