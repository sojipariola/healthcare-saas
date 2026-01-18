# Healthcare SaaS - Quick Start Guide (Heroku)

## 🎯 Quick Links
- **Production App**: https://healthcare-saas-app-83507e23ea58.herokuapp.com/
- **Dashboard**: https://dashboard.heroku.com/apps/healthcare-saas-app
- **GitHub Repo**: Check your git remote: `git remote -v`

---

## ✅ Current Status

```
✅ Web dyno: Running (Gunicorn)
✅ Worker dyno: Running (Celery)
✅ Database: PostgreSQL connected
✅ Cache/Queue: Redis connected (SSL)
✅ Static files: Served by WhiteNoise
```

---

## 🔧 Common Tasks

### Create Admin User
```bash
heroku run python manage.py createsuperuser -a healthcare-saas-app
# Then visit: https://healthcare-saas-app-83507e23ea58.herokuapp.com/admin/
```

### View Logs
```bash
heroku logs --tail -a healthcare-saas-app
# Or just recent errors:
heroku logs -n 50 -a healthcare-saas-app | grep ERROR
```

### Run Database Migrations
```bash
heroku run python manage.py migrate -a healthcare-saas-app
```

### Test Celery Worker
```bash
heroku run python manage.py shell -a healthcare-saas-app
# In Python:
from billing.tasks import daily_trial_expiry_soft_reminder
daily_trial_expiry_soft_reminder.delay()
```

### Restart App
```bash
heroku restart -a healthcare-saas-app
```

### View Environment Config
```bash
heroku config -a healthcare-saas-app
```

### Update Environment Variable
```bash
heroku config:set KEY=value -a healthcare-saas-app
```

---

## 📊 Monitoring

### Check Health Status
```bash
heroku ps -a healthcare-saas-app
```

### Database Size & Connections
```bash
heroku pg:info -a healthcare-saas-app
```

### Redis Stats
```bash
heroku redis:info -a healthcare-saas-app
```

### View Recent Deployments
```bash
heroku releases -a healthcare-saas-app
```

---

## 🚨 Troubleshooting

### App Crashes
1. Check logs: `heroku logs --tail -a healthcare-saas-app`
2. Restart: `heroku restart -a healthcare-saas-app`
3. Check dyno size: `heroku ps -a healthcare-saas-app`

### Worker Crashes
```bash
heroku logs -a healthcare-saas-app -n 100 | grep "worker.1"
```

### Database Connection Issues
```bash
heroku pg:psql -a healthcare-saas-app
# Then: SELECT 1;  (should return OK)
```

### Static Files Not Loading
```bash
heroku run python manage.py collectstatic --noinput -a healthcare-saas-app
```

### Memory/CPU Issues
```bash
heroku dyno:type -a healthcare-saas-app  # Check current type
heroku ps:scale web=1 -a healthcare-saas-app  # Ensure 1 web dyno
```

---

## 🔐 Environment Variables

### Required (Already Set)
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=.herokuapp.com`
- `DJANGO_SECRET_KEY` (auto-generated)
- `DATABASE_URL` (auto-from PostgreSQL add-on)
- `REDIS_URL` (auto-from Redis add-on)

### Optional (Add if Needed)
```bash
# Email
heroku config:set \
  EMAIL_HOST=smtp.sendgrid.net \
  EMAIL_PORT=587 \
  EMAIL_HOST_USER=apikey \
  EMAIL_HOST_PASSWORD=SG.xxxxxx \
  -a healthcare-saas-app

# Stripe
heroku config:set \
  STRIPE_SECRET_KEY=sk_live_xxxxx \
  STRIPE_WEBHOOK_SECRET=whsec_xxxxx \
  -a healthcare-saas-app
```

---

## 📈 Scaling

### Scale Dynos
```bash
# Horizontal scaling (more workers)
heroku ps:scale worker=2 -a healthcare-saas-app  # Add 2nd worker dyno

# Vertical scaling (bigger dyno)
heroku dyno:type web=standard-1x -a healthcare-saas-app  # Upgrade dyno size
```

### Note: Eco Tier Limits
- Max 2 dynos per app (current: 1 web + 1 worker)
- No beat scheduler (use Heroku Scheduler addon)
- Shared CPU, fair-use limits

### Upgrade to Standard
```bash
heroku dyno:type web=standard-1x -a healthcare-saas-app
heroku ps:scale beat=1 -a healthcare-saas-app  # Now you can add beat
```

---

## 🎯 Next Steps Priority

1. **TODAY** - Fix Django BigAutoField warnings (12 total)
2. **THIS WEEK** - Set up Sentry error tracking
3. **BEFORE LAUNCH** - Configure email, test full user flow
4. **ONGOING** - Monitor logs for errors, track performance

See `HEROKU_DEPLOYMENT_REPORT.md` for detailed recommendations.

---

## 📞 Support

- **Heroku Status**: https://status.heroku.com/
- **Heroku Docs**: https://devcenter.heroku.com/
- **Django Docs**: https://docs.djangoproject.com/
- **Celery Docs**: https://docs.celeryproject.io/

---

**Last Updated**: 2026-01-16 12:44 UTC  
**Maintained By**: Healthcare SaaS Team
