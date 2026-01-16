web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
worker: celery -A config worker --loglevel=info
beat: celery -A config beat --loglevel=info