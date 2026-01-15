from django.contrib import admin
from .models import SubscriptionPlan, TenantSubscription, Payment

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "interval", "is_active")
    list_filter = ("interval", "is_active")
    search_fields = ("name",)

@admin.register(TenantSubscription)
class TenantSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("tenant", "plan", "start_date", "end_date", "active")
    list_filter = ("active", "plan")
    search_fields = ("tenant__name", "plan__name")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("tenant", "patient", "amount", "currency", "timestamp", "is_subscription")
    list_filter = ("is_subscription", "currency")
    search_fields = ("tenant__name", "patient__first_name", "patient__last_name")
