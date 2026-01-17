# Healthcare SaaS Platform

Multi-tenant healthcare SaaS platform built with Django. Secure patient management, appointments, clinical records, and billing with HIPAA/GDPR compliance. Encrypted PHI, immutable audit logs, RBAC, FHIR integration, and AI features. Docker containerized with GitHub Actions CI/CD.

## 🏥 Features

### Core Functionality
- **Multi-tenant Architecture**: Isolated data per healthcare organization using PostgreSQL schemas
- **Patient Management**: Comprehensive patient records with encrypted PHI (Protected Health Information)
- **Appointment Scheduling**: Advanced scheduling system with provider availability management
- **Clinical Records**: Electronic Health Records (EHR) with encrypted medical data
- **Billing & Invoicing**: Complete billing system with insurance claims tracking
- **Audit Logging**: Immutable audit trails for all PHI access and modifications

### Security & Compliance
- ✅ **HIPAA Compliant**: Field-level encryption, audit logs, access controls
- ✅ **GDPR Compliant**: Data retention policies, right to be forgotten, consent management
- ✅ **Encrypted PHI**: All sensitive patient data encrypted at rest using AES-256
- ✅ **Immutable Audit Logs**: Complete audit trail that cannot be modified or deleted
- ✅ **RBAC**: Role-Based Access Control with granular permissions
- ✅ **Session Security**: Secure session management with automatic timeout

### Integrations
- **FHIR Integration**: Fast Healthcare Interoperability Resources support
- **REST API**: Comprehensive RESTful API with authentication
- **AI Features**: Ready for AI/ML integration (OpenAI, Langchain support)

### Infrastructure
- **Docker**: Fully containerized application
- **PostgreSQL**: Multi-tenant database with schema isolation
- **Redis**: Caching and task queue support
- **Celery**: Asynchronous task processing
- **GitHub Actions**: Automated CI/CD pipeline

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local development)
- PostgreSQL 16+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/sojipariola/healthcare-saas.git
cd healthcare-saas
```

2. **Create environment file**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Create database schemas**
```bash
docker-compose exec web python manage.py migrate_schemas --shared
```

5. **Create superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

6. **Access the application**
- Admin Panel: http://localhost:8000/admin/
- API: http://localhost:8000/api/
- Health Check: http://localhost:8000/health/

### Local Development

1. **Install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Set up database**
```bash
# Create PostgreSQL database
createdb healthcare_db

# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate
```

3. **Create superuser**
```bash
python manage.py createsuperuser
```

4. **Run development server**
```bash
python manage.py runserver
```

## 📊 Architecture

### Multi-Tenancy
Each healthcare organization (tenant) has its own isolated database schema:
- Public schema: Shared data (tenant definitions, domains)
- Tenant schemas: Isolated patient data, appointments, billing, etc.

### Security Layers
1. **Network Security**: HTTPS only, secure headers
2. **Application Security**: RBAC, session management, CSRF protection
3. **Data Security**: Field-level encryption for PHI
4. **Audit Security**: Immutable logs with blockchain-style integrity

### Data Models

#### Patients
- Encrypted personal information (name, DOB, SSN)
- Encrypted contact details
- Encrypted medical history and allergies
- Insurance information
- Consent management

#### Appointments
- Scheduling with provider availability
- Multiple appointment types
- Status tracking
- Automated reminders

#### Clinical Records
- Encrypted chief complaints and diagnoses
- Vital signs tracking
- Assessment and treatment plans
- ICD-10 coding support
- Immutability for finalized records

#### Billing
- Invoice generation
- Payment tracking
- Insurance claims management
- CPT/HCPCS procedure codes

#### Audit Logs
- All PHI access logged
- User actions tracked
- Immutable after creation
- Security event monitoring

## 🔐 Security Features

### Encryption
All sensitive patient data is encrypted using `django-cryptography`:
- AES-256 encryption
- Separate encryption keys per tenant
- Automatic encryption/decryption

### Audit Logging
Every action is logged with:
- User identity
- Timestamp
- Action type
- Resource accessed
- IP address
- Changes made (before/after)

### Access Control
- Role-based permissions
- Field-level access control
- Audit trail for all PHI access
- Automatic session timeout

## 🔌 API Documentation

### Authentication
```bash
# Token authentication
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

### Patients API
```bash
# List patients
GET /api/patients/

# Create patient
POST /api/patients/
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1980-01-01",
  "gender": "male",
  "email": "john@example.com"
}

# Get patient details
GET /api/patients/{id}/

# Get medical history
GET /api/patients/{id}/medical_history/
```

### FHIR Support
```bash
# Export patient as FHIR resource
GET /api/fhir/Patient/{id}

# Import FHIR resource
POST /api/fhir/import/
```

## 🧪 Testing

### Run tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific app tests
pytest patients/tests/
```

### CI/CD
GitHub Actions automatically runs:
- Code quality checks (flake8, black, isort)
- Security scans (safety, bandit)
- Unit and integration tests
- Docker image builds
- Deployment (on main branch)

## 📝 Development

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations (shared schema)
python manage.py migrate_schemas --shared

# Apply migrations (all tenants)
python manage.py migrate_schemas
```

### Create New Tenant
```bash
python manage.py create_tenant \
  --schema_name=clinic1 \
  --name="Main Street Clinic" \
  --domain=clinic1.localhost
```

## 🌐 FHIR Integration

The platform supports FHIR R4 resources:
- Patient
- Observation
- Condition
- Procedure
- MedicationRequest
- DiagnosticReport
- Encounter

### Sync with FHIR Server
```python
from fhir_integration.services import FHIRService

service = FHIRService()
service.sync_patient(patient_id)
```

## 🤖 AI Features (Optional)

### Enable AI Features
Add to your `.env`:
```
OPENAI_API_KEY=your-api-key
```

### AI Capabilities
- Clinical decision support
- Medical coding assistance (ICD-10 suggestions)
- Natural language processing for clinical notes
- Predictive analytics for patient outcomes

## 📋 Compliance

### HIPAA Requirements
- ✅ Access controls
- ✅ Audit trails
- ✅ Data encryption
- ✅ Emergency access procedures
- ✅ Automatic logoff
- ✅ Unique user identification

### GDPR Requirements
- ✅ Data minimization
- ✅ Purpose limitation
- ✅ Storage limitation
- ✅ Right to access
- ✅ Right to erasure
- ✅ Consent management

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Review and update security settings
- [ ] Perform security audit
- [ ] Set up log aggregation
- [ ] Configure CDN for static files

### Environment Variables
See `.env.example` for all available configuration options.

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Security Guide](docs/security.md)
- [Deployment Guide](docs/deployment.md)
- [FHIR Integration](docs/fhir.md)
- [Compliance Guide](docs/compliance.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

This project is proprietary software. All rights reserved.

## 🔒 Security

To report security vulnerabilities, please email security@healthcare-saas.com

## 📞 Support

For support and questions:
- Documentation: https://docs.healthcare-saas.com
- Issues: GitHub Issues
- Email: support@healthcare-saas.com

## 🙏 Acknowledgments

- Django REST Framework
- django-tenants for multi-tenancy
- FHIR Resources library
- PostgreSQL for reliable data storage

---

**Note**: This is a healthcare application handling sensitive patient data. Ensure all deployments comply with local healthcare regulations (HIPAA, GDPR, etc.).
