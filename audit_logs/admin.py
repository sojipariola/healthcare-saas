from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "action", "user", "tenant", "details")
    list_filter = ("action", "tenant")
    search_fields = ("user__username", "tenant__name", "details")
    ordering = ("-timestamp",)
