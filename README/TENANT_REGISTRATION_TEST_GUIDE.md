# Quick Test Guide: Tenant Registration Feature

## Local Testing

### Setup
```bash
# 1. Apply any migrations
python manage.py migrate

# 2. Run development server
python manage.py runserver

# 3. Open browser
http://localhost:8000/accounts/register/
```

### Test Scenario 1: Create New Company (Happy Path)
**Expected**: User becomes admin immediately, no approval needed

1. Navigate to registration page
2. Select **"Create New Company"** radio button
3. Fill in:
   - Username: `john_doe`
   - Email: `john@example.com`
   - Company Name: `City Medical Clinic`
   - Specialization: `General Practice`
   - Password: `SecurePass123!`
   - Confirm Password: `SecurePass123!`
4. Click **Register**
5. ✅ **Expected**:
   - Success message: "Welcome! Your organization 'City Medical Clinic' has been created. You have a 14-day free trial (up to 2 users, 5 patients)."
   - Redirected to login page
   - Can log in immediately

**Verify in Database**:
```bash
python manage.py shell
```
```python
from users.models import CustomUser
from tenants.models import Tenant

# Check tenant created
tenant = Tenant.objects.get(name='City Medical Clinic')
print(f"Subdomain: {tenant.subdomain}")  # Should be 'city-medical-clinic'
print(f"Plan: {tenant.plan}")  # Should be 'free_trial'
print(f"Specialization: {tenant.specialization}")  # Should be 'general_practice'

# Check user
user = CustomUser.objects.get(username='john_doe')
print(f"Role: {user.role}")  # Should be 'admin'
print(f"Active: {user.is_active}")  # Should be True
print(f"Tenant: {user.tenant.name}")  # Should be 'City Medical Clinic'
```

### Test Scenario 2: Join Existing Company (Happy Path)
**Expected**: User requires admin approval

1. Navigate to registration page
2. Select **"Join Existing Company"** radio button
3. Fill in:
   - Username: `jane_smith`
   - Email: `jane@example.com`
   - Organization: Select `City Medical Clinic` from dropdown
   - Password: `SecurePass123!`
   - Confirm Password: `SecurePass123!`
4. Click **Register**
5. ✅ **Expected**:
   - Info message: "Your account has been created and is pending approval. You will be notified once an administrator approves your access."
   - Email printed to console (check terminal)
   - Cannot log in yet

**Check Console Email**:
Look in terminal for email output:
```
Subject: [ClinicCloud] New User Pending Approval: jane_smith
To: john@example.com
Content-Type: text/plain; charset="utf-8"

Hello Admin,

A new user has requested to join your organization: 'City Medical Clinic'.

User Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Username: jane_smith
  Email: jane@example.com
  Role: user
  Registered: January 14, 2025 at 10:30 AM
  Status: Pending Approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
```

**Verify in Database**:
```python
user = CustomUser.objects.get(username='jane_smith')
print(f"Role: {user.role}")  # Should be 'user'
print(f"Active: {user.is_active}")  # Should be False
print(f"Tenant: {user.tenant.name}")  # Should be 'City Medical Clinic'
```

**Approve User**:
```bash
# Option 1: Django shell
python manage.py shell
```
```python
from users.models import CustomUser
user = CustomUser.objects.get(username='jane_smith')
user.is_active = True
user.save()
```

```bash
# Option 2: Admin panel
# 1. Login as admin (john_doe)
# 2. Go to http://localhost:8000/admin/users/customuser/
# 3. Find jane_smith
# 4. Check "Active" checkbox
# 5. Save
```

Now jane_smith can log in!

### Test Scenario 3: Duplicate Company Name
**Expected**: Error message, no tenant created

1. Navigate to registration page
2. Select **"Create New Company"**
3. Fill in Company Name: `City Medical Clinic` (already exists)
4. Fill in other fields
5. Click **Register**
6. ✅ **Expected**:
   - Error message: "A company with this name already exists."
   - Form reloaded with error
   - No new tenant created

### Test Scenario 4: Free Trial Limit Exceeded
**Expected**: User denied, deleted, error shown

**Setup**:
```python
# Create second user to reach limit
python manage.py shell
```
```python
from users.models import CustomUser
from tenants.models import Tenant
from django.contrib.auth.hashers import make_password

tenant = Tenant.objects.get(name='City Medical Clinic')
user2 = CustomUser.objects.create(
    username='user2',
    email='user2@example.com',
    password=make_password('password'),
    tenant=tenant,
    role='user',
    is_active=True
)
```

**Test**:
1. Try registering 3rd user to join City Medical Clinic
2. ✅ **Expected**:
   - Error: "This organization has reached its free trial user limit (2 users). Please contact the administrator to upgrade the plan."
   - User record deleted
   - No email sent

**Verify**:
```python
# User should NOT exist
CustomUser.objects.filter(username='user3').exists()  # Should be False
```

### Test Scenario 5: Expired Trial
**Expected**: User denied, deleted, error shown

**Setup**:
```python
from datetime import datetime, timedelta
tenant = Tenant.objects.get(name='City Medical Clinic')
tenant.trial_ends = datetime.now() - timedelta(days=1)  # Expired yesterday
tenant.save()
```

**Test**:
1. Try joining City Medical Clinic
2. ✅ **Expected**:
   - Error: "This organization's free trial has expired. Please contact the administrator."
   - User deleted
   - No email sent

### Test Scenario 6: UI Dynamic Fields
**Expected**: Fields show/hide based on radio selection

1. Navigate to registration page
2. Select **"Create New Company"**
   - ✅ Company Name field visible
   - ✅ Specialization dropdown visible
   - ✅ Organization dropdown hidden
   - ✅ Info text: "Create a new organization and start your 14-day free trial..."
3. Select **"Join Existing Company"**
   - ✅ Organization dropdown visible
   - ✅ Company Name field hidden
   - ✅ Specialization dropdown hidden
   - ✅ Info text: "Join an existing organization. Your account will require admin approval..."

### Test Scenario 7: Password Validation
**Expected**: Real-time feedback on password strength

1. Navigate to registration page
2. Type password: `pass`
   - ❌ At least 8 characters (red)
   - ❌ Not a common password (red)
   - ❌ Passwords match (red)
3. Type password: `password`
   - ✅ At least 8 characters (green)
   - ❌ Not a common password (red, because "password" is common)
   - ❌ Passwords match (red)
4. Type password: `SecurePass123!`
   - ✅ At least 8 characters (green)
   - ✅ Not a common password (green)
   - ❌ Passwords match (red)
5. Type confirm password: `SecurePass123!`
   - ✅ All checkmarks green

---

## Heroku Testing

### Setup
```bash
# Set environment variables
heroku config:set SITE_URL=https://healthcare-saas-app-83507e23ea58.herokuapp.com -a healthcare-saas-app

# Open app
heroku open /accounts/register/ -a healthcare-saas-app
```

### Test Create Company
1. Follow Scenario 1 above
2. Verify tenant created:
```bash
heroku run python manage.py shell -a healthcare-saas-app
```
```python
from tenants.models import Tenant
Tenant.objects.filter(name='City Medical Clinic').exists()  # Should be True
```

### Test Join Company
1. Follow Scenario 2 above
2. Check logs for email:
```bash
heroku logs --tail -a healthcare-saas-app
```
3. Approve via Heroku admin panel:
```bash
heroku open /admin/ -a healthcare-saas-app
```

### Configure Real Email (Production)
```bash
# Option 1: SendGrid (Recommended)
heroku addons:create sendgrid:starter -a healthcare-saas-app

# Verify credentials set
heroku config:get SENDGRID_API_KEY -a healthcare-saas-app

# Update Django settings to use SendGrid
# (Already configured if using django-sendgrid-v5)

# Test email
heroku run python manage.py shell -a healthcare-saas-app
```
```python
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test.',
    'noreply@cliniccloud.com',
    ['your-email@example.com'],
    fail_silently=False
)
# Check your inbox
```

---

## Troubleshooting

### Issue: Registration form doesn't show radio buttons
**Solution**: Clear browser cache, check template loaded correctly

### Issue: Fields don't hide/show when clicking radio buttons
**Solution**: Check browser console for JavaScript errors

### Issue: Email not appearing in console
**Solution**: 
- Check EMAIL_BACKEND setting
- Look in Heroku logs: `heroku logs --tail -a healthcare-saas-app`

### Issue: User created but can't log in (join scenario)
**Solution**: This is expected! Admin must approve first. Check is_active field.

### Issue: "Company already exists" even with new name
**Solution**: Check database, might be case-sensitivity issue or whitespace

### Issue: Free trial limit error with only 1 user
**Solution**: Count includes inactive users. Check:
```python
CustomUser.objects.filter(tenant=tenant).count()
```

---

## Database Queries for Verification

```bash
python manage.py shell
```

```python
from users.models import CustomUser
from tenants.models import Tenant

# List all tenants
for t in Tenant.objects.all():
    print(f"{t.name} ({t.subdomain}) - Plan: {t.plan} - Users: {t.customuser_set.count()}")

# List all users with details
for u in CustomUser.objects.all():
    print(f"{u.username} - {u.email} - Tenant: {u.tenant.name} - Role: {u.role} - Active: {u.is_active}")

# Check specific tenant user count
tenant = Tenant.objects.get(name='City Medical Clinic')
print(f"Active users: {CustomUser.objects.filter(tenant=tenant, is_active=True).count()}")
print(f"Pending users: {CustomUser.objects.filter(tenant=tenant, is_active=False).count()}")

# List pending approvals
for u in CustomUser.objects.filter(is_active=False):
    print(f"Pending: {u.username} wants to join {u.tenant.name}")
```

---

## Clean Up Test Data

```python
# Delete test tenant and all users
tenant = Tenant.objects.get(name='City Medical Clinic')
tenant.delete()  # CASCADE deletes all users too

# Or delete specific user
user = CustomUser.objects.get(username='jane_smith')
user.delete()
```

---

## Success Criteria Checklist

- [ ] Can create new company with valid data
- [ ] New company owner is admin and active
- [ ] Can join existing company
- [ ] Joiner is user role and inactive
- [ ] Email sent to admins when user joins
- [ ] Admin can approve user via admin panel
- [ ] Approved user can log in
- [ ] Duplicate company name rejected
- [ ] 3rd user rejected during trial
- [ ] Expired trial prevents joins
- [ ] UI fields show/hide correctly
- [ ] Password validation works
- [ ] Subdomain auto-generated correctly
- [ ] Trial dates set correctly

**Status**: Ready for testing! 🚀
