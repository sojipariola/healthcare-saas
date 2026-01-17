<<<<<<< HEAD
# Healthcare SaaS Platform

A multi-tenant healthcare Software-as-a-Service (SaaS) platform built with Django, designed for managing patient care, appointments, clinical records, and billing while maintaining strict HIPAA, GDPR, and NHS compliance.

## Overview

Healthcare SaaS is a modern, secure healthcare management system designed for clinics, hospitals, and healthcare providers. It provides comprehensive features for:

- **Patient Management**: Secure patient records with PHI encryption
- **Appointment Scheduling**: Conflict detection and async notifications
- **Clinical Records**: SOAP notes with record locking and immutability
- **Lab Management**: Order processing and encrypted results
- **Billing & Payments**: Stripe integration with subscription management
- **Audit Logging**: Immutable audit trails for compliance
- **Multi-tenant Architecture**: Complete tenant isolation
- **FHIR Integration**: Healthcare interoperability standards
- **AI-Powered Features**: Deidentification, summarization, and risk flagging
- **Role-Based Access Control (RBAC)**: Granular permission management

## Key Features

### Security & Compliance
- **Field-level encryption** for all PHI (Protected Health Information)
- **Immutable audit logs** for all data access and modifications
- **HIPAA compliance** with automated audit trail generation
- **GDPR support** with consent management and data retention policies
- **NHS-compliant** security controls
- **Multi-tenant isolation** at model, manager, and middleware layers
- **Threat modeling** and incident response procedures

### Architecture
- **Modular Django apps**: Each domain (tenants, users, patients, etc.) is a separate app
- **Tenant-aware models & managers**: Automatic tenant filtering
- **Custom authentication backend**: Tenant-aware user authentication
- **Abstracted integrations**: Stripe, FHIR, AI services are decoupled
- **Scalable design**: Ready for Docker, Kubernetes, and cloud deployment

### Core Modules
- **tenants/**: Multi-tenant support with subdomain/header-based resolution
- **users/**: Custom user model with RBAC and permission matrix
- **patients/**: Encrypted patient records with permissions
- **appointments/**: Scheduling with conflict detection
- **clinical_records/**: SOAP notes with immutable record locking
- **labs/**: Lab orders and encrypted results
- **billing/**: Stripe integration with subscription management
- **audit_logs/**: Automatic immutable audit logging
- **ai/**: Deidentification, summarization, risk flags
- **fhir/**: FHIR resource serialization and API endpoints
- **compliance/**: GDPR/HIPAA/NHS consent, retention, access requests

## Tech Stack

### Backend
- **Django 6.0+**: Web framework
- **Python 3.11+**: Language
- **PostgreSQL 15**: Primary database
- **Celery**: Asynchronous task queue
- **Redis**: Task broker and caching
- **Gunicorn**: Production WSGI server

### Frontend (Current)
- **Django Templates**: Server-rendered HTML
- **JavaScript/CSS**: Interactivity and styling

### Frontend (Planned)
- **React/TypeScript**: SPA for modern UX
- **Django REST Framework**: API endpoints

### DevOps & CI/CD
- **Docker & Docker Compose**: Containerization
- **GitHub Actions**: CI/CD pipeline
- **GitHub Container Registry**: Image storage
- **Trivy & Bandit**: Security scanning
- **pytest & pytest-django**: Testing framework

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sojipariola/healthcare_saas.git
   cd healthcare_saas
=======
# healthcare-saas
Multi-tenant healthcare SaaS platform built with Django. Secure patient management, appointments, clinical records, and billing with HIPAA/GDPR compliance. Encrypted PHI, immutable audit logs, RBAC, FHIR integration, and AI features. Docker containerized with GitHub Actions CI/CD.
>>>>>>> e19b986 (Initial commit)
