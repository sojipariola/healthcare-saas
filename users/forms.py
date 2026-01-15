from django import forms
from django.contrib.auth.forms import AuthenticationForm
from tenants.models import Tenant

class TenantAwareAuthenticationForm(AuthenticationForm):
    tenant = forms.CharField(label="Tenant", max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        tenant_identifier = cleaned_data.get("tenant")
        try:
            tenant = Tenant.objects.get(name=tenant_identifier)
        except Tenant.DoesNotExist:
            raise forms.ValidationError("Invalid tenant identifier.")
        self.cleaned_data["tenant_obj"] = tenant
        return self.cleaned_data
