from audit_logs.models import AuditLog

def log_audit(action, user=None, tenant=None, details=None):
    AuditLog.objects.create(
        action=action,
        user=user,
        tenant=tenant,
        details=details or ""
    )
