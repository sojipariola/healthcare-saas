from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from audit_logs.models import AuditLog

@login_required
def audit_log_list(request):
    logs = AuditLog.objects.all().order_by('-timestamp')[:100]
    return render(request, "audit_logs/list.html", {"logs": logs})
