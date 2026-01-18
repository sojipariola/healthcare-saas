# Tenant/Company Registration Enhancement

## Overview
Enhanced the user registration system to support two distinct registration flows:
1. **Create New Company**: Users can create their own organization and become instant administrators
2. **Join Existing Company**: Users can request to join existing organizations with admin approval

## Features Implemented

### 1. Dual-Mode Registration Form
**File**: `users/registration_forms.py`

**New Fields**:
- `registration_type`: Radio button choice (Create New Company / Join Existing Company)
- `company_name`: Text field for new company name (required for 'create' mode)
- `specialization`: Dropdown with 25 medical specialization options (required for 'create' mode)
- `tenant`: Dropdown to select existing company (required for 'join' mode)

**Validation Logic**:
- Ensures company_name is unique when creating
- Validates that all required fields are filled based on registration_type
- Automatically generates unique subdomain from company name

**Save Logic**:
- **Create Mode**:
  - Creates new Tenant with auto-generated subdomain
  - Sets user as 'admin' role
  - Auto-activates user (is_active=True)
  - Starts 14-day free trial
- **Join Mode**:
  - Assigns user to selected tenant
  - Sets user as 'user' role
  - User is NOT activated (is_active=False)
  - Requires admin approval

### 2. Enhanced Registration View
**File**: `users/views.py`

**Registration Flow**:
1. Detects registration_type from form
2. **Create Path**:
   - Displays success message with trial information
   - Redirects to login (user can immediately access)
3. **Join Path**:
   - Validates free trial limits (max 2 users during trial)
   - Checks trial expiry status
   - Sends email notification to all company admins
   - Displays pending approval message
   - Deletes user if company at trial limits or trial expired

### 3. Email Notification System
**File**: `users/notifications.py`

**Functions**:

#### `notify_admins_of_new_user(user)`
- Triggered when user joins existing organization
- Sends email to all active admins in the tenant
- Includes user details, registration timestamp, approval link
- Professional email template with security reminder

#### `notify_user_approved(user)` (NEW)
- Notifies user when their account is approved
- Provides login link and account details
- Welcome message

#### `notify_user_rejected(user, reason="")` (NEW)
- Notifies user when account request is rejected
- Optional rejection reason
- Professional closure message

**Email Template Features**:
- Professional branding (ClinicCloud)
- Clear formatting with visual separators
- Actionable links (admin dashboard, login page)
- Security reminders about HIPAA compliance
- Error handling with logging (doesn't block registration on email failure)

### 4. Enhanced Registration Template
**File**: `templates/registration/register.html`

**Features**:
- Radio button selection for registration type
- Dynamic field visibility using JavaScript
- Context-sensitive information text that updates based on selection
- Password strength validation (preserved)
- Clear visual separation between create and join modes
- Responsive form layout with proper labels and help text

**JavaScript Functionality**:
- `updateVisibility()`: Shows/hides fields based on registration_type
- Updates information text dynamically:
  - Create: "Create a new organization and start your 14-day free trial..."
  - Join: "Join an existing organization. Your account will require admin approval..."
- Password validation with real-time feedback

### 5. Configuration Updates
**File**: `config/settings.py`

**New Setting**:
```python
SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000")
```
- Used in email templates for absolute URLs
- Defaults to localhost for development
- Can be overridden with environment variable

## User Experience Flow

### Scenario 1: Creating New Company
1. User visits registration page
2. Selects "Create New Company" radio button
3. Fills in username, email, company name, specialization, passwords
4. Submits form
5. **Result**:
   - New tenant created with unique subdomain
   - User assigned as admin
   - User immediately activated
   - 14-day free trial starts
   - Success message displayed
   - Redirected to login
   - Can immediately access the system

### Scenario 2: Joining Existing Company
1. User visits registration page
2. Selects "Join Existing Company" radio button
3. Fills in username, email, selects company from dropdown, passwords
4. Submits form
5. **System Checks**:
   - Validates company not expired
   - Checks free trial user limits (max 2 during trial)
6. **If Valid**:
   - User created but NOT activated
   - All company admins receive email notification
   - User sees "Your account is pending approval" message
   - User cannot log in yet
7. **Admin Approval**:
   - Admin receives email with user details
   - Admin logs into admin dashboard
   - Admin activates user account
   - (Optional) Admin can trigger `notify_user_approved()` email

### Scenario 3: Joining Company at Trial Limit
1. User attempts to join company during trial
2. Company already has 2 users (trial limit)
3. **Result**:
   - Error message: "This organization has reached its free trial user limit"
   - User record deleted
   - No email sent
   - User redirected back to registration form

## Technical Details

### Subdomain Generation Algorithm
```python
def _generate_unique_subdomain(base_name):
    # Convert to lowercase, replace spaces/special chars with hyphens
    subdomain = base_name.lower().strip()
    subdomain = ''.join(c if c.isalnum() else '-' for c in subdomain)
    subdomain = '-'.join(filter(None, subdomain.split('-')))
    
    # Ensure uniqueness by appending numbers if needed
    if Tenant.objects.filter(subdomain=subdomain).exists():
        counter = 1
        while Tenant.objects.filter(subdomain=f"{subdomain}-{counter}").exists():
            counter += 1
        subdomain = f"{subdomain}-{counter}"
    
    return subdomain[:50]  # Max 50 characters
```

### Free Trial Validation
```python
# Check if tenant at trial limits
if tenant.plan == 'free_trial':
    user_count = CustomUser.objects.filter(tenant=tenant).count()
    if user_count >= 2:
        new_user.delete()
        messages.error(request, 
            "This organization has reached its free trial user limit (2 users). "
            "Please contact the administrator to upgrade the plan."
        )
        return redirect('users:register')
```

### Email Error Handling
```python
try:
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to send admin notification email: {str(e)}")
    # Registration continues even if email fails
```

## Environment Variables

### Required for Production
```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net  # or other SMTP provider
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-username
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@cliniccloud.com

# Site URL for email links
SITE_URL=https://healthcare-saas-app-83507e23ea58.herokuapp.com
```

### For Development (defaults already set)
```bash
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
SITE_URL=http://localhost:8000
```

## Testing Checklist

### Test Case 1: Create New Company
- [ ] Submit form with valid company name
- [ ] Verify tenant created in database
- [ ] Verify user has 'admin' role
- [ ] Verify user is_active=True
- [ ] Verify trial dates set correctly
- [ ] Verify unique subdomain generated
- [ ] Verify redirect to login
- [ ] Verify user can log in immediately

### Test Case 2: Join Existing Company
- [ ] Submit form selecting existing tenant
- [ ] Verify user created with 'user' role
- [ ] Verify user is_active=False
- [ ] Verify email sent to admins
- [ ] Verify user cannot log in yet
- [ ] Admin activates user in admin panel
- [ ] Verify user can now log in

### Test Case 3: Company Name Validation
- [ ] Try creating company with duplicate name
- [ ] Verify error message displayed
- [ ] Verify no tenant created

### Test Case 4: Free Trial Limits
- [ ] Create tenant with 2 users
- [ ] Try adding 3rd user via join
- [ ] Verify error message
- [ ] Verify user deleted
- [ ] Verify no email sent

### Test Case 5: Expired Trial
- [ ] Set tenant trial_ends to past date
- [ ] Try joining that tenant
- [ ] Verify error message
- [ ] Verify user deleted

### Test Case 6: Email Functionality
- [ ] Configure SMTP or SendGrid
- [ ] Submit join request
- [ ] Verify email received by admins
- [ ] Verify email formatting correct
- [ ] Verify links in email work

### Test Case 7: Template Display
- [ ] Visit registration page
- [ ] Verify both radio buttons display
- [ ] Select "Create" - verify create fields show
- [ ] Select "Join" - verify join fields show
- [ ] Verify info text updates correctly
- [ ] Verify password validation still works

## Known Issues & Limitations

### Current Limitations:
1. **Email Backend**: Currently using console backend (emails printed to console)
   - **Solution**: Configure SMTP provider for production (SendGrid, Mailgun, AWS SES)

2. **Admin Approval UI**: Admins must use Django admin panel to approve users
   - **Future Enhancement**: Create custom approval dashboard

3. **No Email on Approval**: `notify_user_approved()` not automatically triggered
   - **Future Enhancement**: Add Django signal or admin action to trigger email

4. **Subdomain Not Used Yet**: Generated subdomains not actively used for routing
   - **Future Enhancement**: Implement subdomain-based tenant resolution

### Future Enhancements:
- [ ] Add custom approval dashboard for admins
- [ ] Implement Django signals to auto-send approval emails
- [ ] Add bulk user approval functionality
- [ ] Create tenant switching UI for multi-tenant users
- [ ] Implement subdomain-based routing
- [ ] Add company/tenant search functionality
- [ ] Add invitation system (invite-only registration)
- [ ] Add SSO/SAML integration for enterprise plans

## Files Modified

1. **users/registration_forms.py** - Complete rewrite of registration form
2. **users/views.py** - Enhanced registration view logic
3. **users/notifications.py** - Added comprehensive email notification system
4. **templates/registration/register.html** - Enhanced UI with dynamic fields
5. **config/settings.py** - Added SITE_URL configuration

## Database Impact

### New Tenant Records Created:
- Auto-generated subdomain based on company name
- Specialization field populated
- Trial dates set automatically
- Plan set to 'free_trial'

### User Records:
- role field: 'admin' for creators, 'user' for joiners
- is_active field: True for creators, False for joiners
- tenant FK: Links to new or existing tenant

## Security Considerations

### Implemented:
- ✅ Company name uniqueness validation
- ✅ Free trial limit enforcement
- ✅ Admin approval requirement for joiners
- ✅ Email notifications to admins
- ✅ HIPAA compliance reminder in emails
- ✅ Secure password validation preserved
- ✅ CSRF protection preserved

### Recommendations:
- Configure HTTPS for production (Heroku SSL)
- Implement rate limiting on registration endpoint
- Add CAPTCHA for public registration
- Monitor for suspicious registration patterns
- Implement email verification before approval
- Add 2FA for admin accounts

## Deployment Notes

### Heroku Environment Variables to Set:
```bash
heroku config:set SITE_URL=https://healthcare-saas-app-83507e23ea58.herokuapp.com -a healthcare-saas-app
heroku config:set DEFAULT_FROM_EMAIL=noreply@cliniccloud.com -a healthcare-saas-app

# If using SendGrid
heroku addons:create sendgrid:starter -a healthcare-saas-app
# SendGrid API key will be auto-set as SENDGRID_API_KEY

# If using Mailgun
heroku addons:create mailgun:starter -a healthcare-saas-app
```

### Verify Deployment:
```bash
# Push changes
git add .
git commit -m "feat: Enhanced tenant registration with create/join modes"
git push heroku main

# Run migrations (if any)
heroku run python manage.py migrate -a healthcare-saas-app

# Test registration
heroku open -a healthcare-saas-app
```

## Support & Troubleshooting

### Common Issues:

**Issue**: Email not sending
- **Check**: EMAIL_BACKEND setting
- **Solution**: Configure SMTP provider or check console backend logs

**Issue**: User can't log in after joining company
- **Check**: is_active field in database
- **Solution**: Admin must approve user first

**Issue**: "Company already exists" error
- **Check**: Tenant.name uniqueness
- **Solution**: Choose different company name

**Issue**: JavaScript not working (fields not hiding/showing)
- **Check**: Browser console for errors
- **Solution**: Ensure jQuery loaded, check template syntax

**Issue**: Free trial limit error even with < 2 users
- **Check**: Count includes inactive users
- **Solution**: Delete inactive test users or upgrade plan

## API Documentation (Future)

When API endpoints are added, they should support:
- `POST /api/register/` - Dual-mode registration
- `GET /api/tenants/` - List available tenants for joining
- `POST /api/tenants/{id}/approve/{user_id}/` - Admin approval endpoint
- `GET /api/tenants/{id}/pending-users/` - List pending users for admin

## Related Documentation
- [Multi-Tenant Architecture](/.github/copilot-instructions.md)
- [Free Trial System](/billing/README.md)
- [RBAC Permissions](/users/permissions.py)
- [Email Configuration](/config/settings.py)
- [Heroku Deployment](/HEROKU_DEPLOYMENT_REPORT.md)

---
**Last Updated**: January 2025
**Feature Status**: ✅ Implemented, ⏳ Pending Testing
**Priority**: HIGH - Core Registration Feature
