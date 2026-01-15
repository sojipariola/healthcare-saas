from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser

def notify_admins_of_new_user(user):
    admins = CustomUser.objects.filter(tenant=user.tenant, role='admin', is_active=True)
    if not admins:
        return
    subject = f"[Healthcare SaaS] New User Approval Needed: {user.username} ({user.email})"
    message = (
        f"Hello Admin,\n\n"
        f"A new user has registered for your organization ('{user.tenant}').\n\n"
        f"User Details:\n"
        f"- Username: {user.username}\n"
        f"- Email: {user.email}\n"
        f"- Registered: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"To approve this user, please log in to the admin dashboard:\n"
        f"https://{{your-domain}}/admin/users/customuser/\n\n"
        f"Thank you,\nHealthcare SaaS Team"
    )
    from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'webmaster@localhost'
    recipient_list = [admin.email for admin in admins if admin.email]
    if recipient_list:
        send_mail(subject, message, from_email, recipient_list)
