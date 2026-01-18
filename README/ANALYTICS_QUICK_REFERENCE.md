# 📊 Analytics Module - Quick Reference Card

## 🚀 Quick Access

### URLs
| Dashboard | URL | Purpose |
|-----------|-----|---------|
| Main | `/analytics/` | Overview KPIs |
| Executive | `/analytics/executive/` | Strategic insights |
| Patients | `/analytics/patients/` | Demographics |
| Appointments | `/analytics/appointments/` | Scheduling |
| Revenue | `/analytics/revenue/` | Financials |
| Users | `/analytics/users/` | Engagement |

## 🔐 Access Requirements

✅ **Required**:
- Professional OR Enterprise subscription
- Admin role
- Logged in

❌ **Blocked**:
- Free Trial (→ redirects to upgrade)
- Starter Plan (→ redirects to upgrade)
- Non-admin users

## 🎯 Quick Setup

```bash
# 1. Upgrade tenant
python3 manage.py shell
from tenants.models import Tenant
t = Tenant.objects.get(name='YourClinic')
t.plan = 'professional'
t.save()

# 2. Make user admin
from users.models import CustomUser
u = CustomUser.objects.get(username='youruser')
u.role = 'admin'
u.save()

# 3. Visit analytics
# http://localhost:8000/analytics/
```

## 📊 Key Metrics

### Patient Metrics
- Total patients
- New patients (30d)
- Active patients (90d)
- Age distribution

### Appointment Metrics
- Monthly count
- Upcoming count
- Completion rate
- Day-of-week patterns

### Financial Metrics
- Total revenue
- Monthly revenue
- Average payment
- Top patients

### System Metrics
- Clinical records
- Lab results
- Active users
- System events

## 🎨 Chart Types

| Type | Use Case | Dashboards |
|------|----------|------------|
| Line | Trends over time | Patients, Revenue, Users |
| Bar | Monthly/weekly comparisons | Appointments |
| Pie/Doughnut | Status/age distributions | Patients, Appointments |
| Table | Rankings, details | All |

## 💡 Pro Tips

1. **Cache Queries**: Set `ANALYTICS_CACHE_TIMEOUT=3600`
2. **Sample Data**: Use shell to create test events
3. **Export**: PDF feature coming in Phase 2
4. **Mobile**: Fully responsive design
5. **Customization**: Edit templates in `templates/analytics/`

## 🐛 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Access denied | Check role = 'admin' |
| Need upgrade | Check plan = 'professional' or 'enterprise' |
| No charts | Check Chart.js loaded, check browser console |
| No data | Create sample events or wait for usage |

## 📚 Documentation

- **Full Docs**: `analytics/README.md`
- **Setup Guide**: `ANALYTICS_SETUP.md`
- **Summary**: `ANALYTICS_IMPLEMENTATION_SUMMARY.md`

## 🔧 Developer Quick Ref

### Track Custom Event
```python
from analytics.models import AnalyticsEvent

AnalyticsEvent.objects.create(
    tenant=request.user.tenant,
    event_type='custom_event',
    user_id=request.user.id,
    metadata={'key': 'value'}
)
```

### Add Custom View
```python
from analytics.decorators import admin_or_analytics_access

@admin_or_analytics_access
def my_analytics(request):
    tenant = request.user.tenant
    # Your logic
    return render(request, 'analytics/my_view.html', context)
```

### Add URL Route
```python
# config/urls.py
path('analytics/custom/', my_analytics, name='my_custom'),
```

## ✅ Status Check

```bash
# Verify installation
python3 manage.py check

# Check migrations
python3 manage.py showmigrations analytics

# Run server
python3 manage.py runserver
```

## 📞 Support

- Check Django logs
- Review `analytics/README.md`
- Test with sample data
- Verify tenant plan and user role

---

**Version**: 1.0  
**Status**: ✅ Production Ready  
**Subscription**: Professional & Enterprise  
**Last Updated**: January 2026
