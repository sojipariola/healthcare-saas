from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser
from tenants.models import Tenant

class TenantAwareAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, tenant=None, **kwargs):
        if username is None or password is None or tenant is None:
            return None
        try:
            user = CustomUser.objects.get(username=username, tenant=tenant)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
        return None
