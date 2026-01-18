# Analytics Module - Quick Setup Guide

## ✅ Installation Complete!

The analytics module has been successfully configured with the following features:

### 🎯 What's Included

**6 Analytics Dashboards**:
1. **Main Dashboard** (`/analytics/`) - KPIs overview
2. **Executive Summary** (`/analytics/executive/`) - High-level insights
3. **Patient Analytics** (`/analytics/patients/`) - Demographics & growth
4. **Appointment Analytics** (`/analytics/appointments/`) - Scheduling patterns
5. **Revenue Analytics** (`/analytics/revenue/`) - Financial performance
6. **User Activity** (`/analytics/users/`) - System usage

### 🔐 Access Control

**Subscription Requirements**:
- ✅ Professional Plan
- ✅ Enterprise Plan
- ❌ Free Trial (redirects to upgrade)
- ❌ Starter Plan (redirects to upgrade)

**User Requirements**:
- Must be admin role
- Must be logged in

### 🚀 Quick Start

**1. Upgrade a tenant to Professional plan**:
```bash
python3 manage.py shell
```
```python
from tenants.models import Tenant
tenant = Tenant.objects.get(name='Your Clinic Name')
tenant.plan = 'professional'  # or 'enterprise'
tenant.save()
exit()
```

**2. Make user an admin**:
```python
from users.models import CustomUser
user = CustomUser.objects.get(username='youruser')
user.role = 'admin'
user.save()
```

**3. Start the server**:
```bash
python3 manage.py runserver
```

**4. Visit analytics**:
```
http://localhost:8000/analytics/
```

### 📊 Database Migrations

✅ Migrations applied successfully:
- `analytics/migrations/0002_*.py` - Model indexes and improvements
- `tenants/migrations/0004_*.py` - BigAutoField updates

### 🎨 Features

**Visual Components**:
- 📈 Chart.js 4.4.0 interactive charts
- 🎨 Modern gradient design
- 📱 Responsive (mobile-friendly)
- 🔄 Real-time data aggregation

**Data Sources**:
- Patients
- Appointments
- Clinical Records
- Lab Results
- Payments
- User Activity
- Analytics Events

**Chart Types**:
- Line charts (trends)
- Bar charts (comparisons)
- Pie/Doughnut charts (distributions)
- Tables with visualizations

### 📝 Testing Checklist

- [ ] Create Professional/Enterprise tenant
- [ ] Assign admin user
- [ ] Visit `/analytics/`
- [ ] Check KPI cards display correctly
- [ ] Navigate to Executive Summary
- [ ] Test Patient Analytics charts
- [ ] Test Appointment Analytics
- [ ] Test Revenue Analytics
- [ ] Test User Activity Analytics

### 🔧 Configuration

**Environment Variables** (optional):
```bash
# Cache analytics queries (recommended for production)
ANALYTICS_CACHE_TIMEOUT=3600  # 1 hour

# Data retention
ANALYTICS_RETENTION_DAYS=730  # 2 years
```

**Django Settings**:
```python
# config/settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Recommended
```

### 📚 Documentation

Full documentation available at:
- `analytics/README.md` - Complete module documentation
- `/analytics/` dashboard - Interactive help
- Comments in code

### 🐛 Troubleshooting

**Issue**: "Module not found" errors
**Solution**: Install dependencies
```bash
pip3 install -r requirements.txt
```

**Issue**: Charts not displaying
**Solution**: Check browser console, ensure Chart.js loaded

**Issue**: Access denied
**Solution**: Check user role and tenant plan:
```python
# User must be admin
user.role = 'admin'
# Tenant must be Professional/Enterprise
tenant.plan = 'professional'
```

**Issue**: No data in analytics
**Solution**: Create some test data or wait for real usage

### 🎯 Next Steps

1. **Generate sample data** (optional):
   ```bash
   python3 manage.py shell
   ```
   ```python
   from analytics.models import AnalyticsEvent
   from django.utils import timezone
   from datetime import timedelta
   
   tenant = Tenant.objects.first()
   for i in range(100):
       AnalyticsEvent.objects.create(
           tenant=tenant,
           event_type='patient_view',
           user_id=1,
           timestamp=timezone.now() - timedelta(days=i % 30)
       )
   ```

2. **Customize dashboards**: Edit templates in `templates/analytics/`

3. **Add custom metrics**: Create new views in `analytics/views.py`

4. **Track custom events**: Use `AnalyticsEvent.objects.create()` in your views

5. **Deploy to production**: 
   - Configure caching
   - Set up CDN for Chart.js
   - Optimize database indexes

### 🌟 Key URLs

| URL | Description |
|-----|-------------|
| `/analytics/` | Main dashboard |
| `/analytics/executive/` | Executive summary |
| `/analytics/patients/` | Patient analytics |
| `/analytics/appointments/` | Appointment analytics |
| `/analytics/revenue/` | Revenue analytics |
| `/analytics/users/` | User activity |
| `/billing/plans/` | Upgrade page |

### 💡 Pro Tips

1. **Performance**: Analytics queries are optimized with indexes
2. **Security**: All data is tenant-isolated automatically
3. **Privacy**: No PHI in analytics metadata
4. **Customization**: Easy to extend with new views
5. **Export**: Future feature - PDF/Excel exports coming

### 📞 Support

For issues or questions:
1. Check `analytics/README.md`
2. Review code comments
3. Test with sample data
4. Check Django logs

---

**Status**: ✅ Ready for use
**Version**: 1.0
**Subscription**: Professional & Enterprise only
**Last Updated**: January 2026
