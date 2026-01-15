from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from tenants.models import Tenant

class TenantUserRegistrationForm(UserCreationForm):
    tenant = forms.ModelChoiceField(queryset=Tenant.objects.all(), label="Tenant", required=True)
    email = forms.EmailField(required=True)
    role = forms.CharField(label="Role", max_length=50, required=False)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "tenant", "role", "password1", "password2")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match. Please re-enter.")
            if password1.lower() in ["password", "123456", "qwerty", "letmein"]:
                raise forms.ValidationError("This password is too common. Please choose a stronger password.")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tenant = self.cleaned_data["tenant"]
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data.get("role", "user")
        user.is_active = False  # Require admin approval
        if commit:
            user.save()
        return user
