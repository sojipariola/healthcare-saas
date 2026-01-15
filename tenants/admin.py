
from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "subdomain", "created_at", "updated_at")
	search_fields = ("name", "subdomain")
