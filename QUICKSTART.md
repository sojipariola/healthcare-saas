# Quick Start Guide

Get the Healthcare SaaS Platform running in 5 minutes!

## Option 1: Using Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Git

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/sojipariola/healthcare-saas.git
cd healthcare-saas
```

2. **Set up environment**
```bash
cp .env.example .env
# Edit .env with your preferred settings (optional for development)
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Create database schemas**
```bash
docker-compose exec web python manage.py migrate_schemas --shared
```

5. **Create a superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Create your first tenant**
```bash
docker-compose exec web python manage.py create_tenant \
  --schema_name=demo_clinic \
  --name="Demo Clinic" \
  --domain=demo.localhost \
  --organization_type=clinic
```

7. **Access the application**
- Admin Panel: http://localhost:8000/admin/
- API: http://localhost:8000/api/
- Health Check: http://localhost:8000/health/

## Option 2: Local Development

### Prerequisites
- Python 3.12+
- PostgreSQL 16+
- Redis (optional, for Celery)

### Steps

1. **Clone and setup**
```bash
git clone https://github.com/sojipariola/healthcare-saas.git
cd healthcare-saas
```

2. **Run setup script**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Activate virtual environment**
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Configure database**
Edit `.env` file:
```
DATABASE_NAME=healthcare_db
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

## Common Commands

Using Make:
```bash
make help           # Show all available commands
make install        # Install dependencies
make test           # Run tests
make lint           # Check code quality
make format         # Format code
make docker-up      # Start Docker containers
make docker-down    # Stop Docker containers
```

Using Django directly:
```bash
python manage.py runserver              # Start development server
python manage.py migrate                # Run migrations
python manage.py createsuperuser        # Create admin user
python manage.py test                   # Run tests
python manage.py shell                  # Open Django shell
```

## First API Request

After starting the server, try the health check:

```bash
curl http://localhost:8000/health/
```

Expected response:
```json
{"status": "healthy"}
```

## Authentication

Get an authentication token:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Use the token for API requests:

```bash
curl http://localhost:8000/api/patients/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Sample API Requests

### Create a Patient
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1980-01-01",
    "gender": "male",
    "email": "john.doe@example.com",
    "phone": "555-0100",
    "consent_to_treat": true,
    "hipaa_consent": true
  }'
```

### List Patients
```bash
curl http://localhost:8000/api/patients/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify PostgreSQL is listening on the correct port

### Import Errors
- Activate virtual environment
- Run `pip install -r requirements.txt`

### Docker Issues
- Run `docker-compose down -v` to clean up
- Run `docker-compose up -d --build` to rebuild

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Check [SECURITY.md](SECURITY.md) for security best practices
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
4. Explore the API documentation at `/api/`

## Need Help?

- Check the [README.md](README.md) for detailed information
- Open an issue on GitHub
- Review the Django documentation

---

🎉 **Congratulations!** Your Healthcare SaaS Platform is now running!
