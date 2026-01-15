from django.contrib import admin
from .models import AnalyticsEvent

@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("event_type", "tenant", "user_id", "timestamp")
    search_fields = ("event_type", "user_id")
    list_filter = ("event_type", "tenant")
