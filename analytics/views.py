from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import AnalyticsEvent
from tenants.models import Tenant
from users.models import CustomUser
from django.db.models import Count

def is_admin(user):
    return user.is_superuser or getattr(user, 'role', None) == 'admin'

@login_required
@user_passes_test(is_admin)
def analytics_dashboard(request):
    tenant = request.user.tenant
    # Example: event counts by type
    event_counts = AnalyticsEvent.objects.filter(tenant=tenant).values('event_type').annotate(count=Count('id')).order_by('-count')
    # Example: user activity
    user_activity = AnalyticsEvent.objects.filter(tenant=tenant).values('user_id').annotate(count=Count('id')).order_by('-count')
    users = {u.id: u for u in CustomUser.objects.filter(id__in=[ua['user_id'] for ua in user_activity])}
    return render(request, "analytics/dashboard.html", {
        "event_counts": event_counts,
        "user_activity": user_activity,
        "users": users,
    })
