# Healthcare SaaS - AI Coding Instructions

## Project Overview
Multi-tenant healthcare SaaS platform with strict PHI, audit, and compliance requirements.
Modular Django-based architecture: each domain (tenants, users, patients, appointments, etc.) is a separate app.
All business logic is outside config/; config/ only for project wiring and global settings.

## Architecture
- **config/**: Project config, global middleware, settings (security, auth, logging, DB, AI, FHIR, celery, tenants)
- **common/**: Shared utilities (encryption, audit, RBAC, tenant-aware models/managers)
- **tenants/**: Tenant model, resolution, isolation (subdomain/header)
- **users/**: Custom user, roles, RBAC, permission matrix
- **patients/**: PHI, encrypted models, patient permissions
- **appointments/**: Scheduling, conflict detection, async notifications
- **clinical_records/**: SOAP notes, record locking, immutable records
- **labs/**: Orders, encrypted results
- **referrals/**: Whitelisting, referral rules
- **documents/**: Imaging, secure storage abstraction
- **audit_logs/**: Immutable audit logs, automatic capture
- **billing/**: Plans, Stripe integration, enforcement
- **cms/**: Content, NO PHI
- **notifications/**: Email, SMS, push, async tasks
- **ai/**: Deidentification, summarisation, risk flags, review flow
- **fhir/**: FHIR resources, serializers, views
- **security/**: Threat modeling, secrets (Vault/KMS), monitoring, incident response
- **compliance/**: GDPR/HIPAA/NHS, consent, retention, access requests, breach
- **tests/**: System-wide, tenant isolation, security, permissions, audit

## Data & Security Patterns
- All PHI is encrypted at rest (see common/encryption.py, patients/models.py, labs/models.py)
- Audit logging is automatic and immutable (audit_logs/, common/audit.py, middleware)
- Tenant isolation enforced at model, manager, and middleware layers
- RBAC via common/permissions.py, users/roles.py, users/permissions.py
- Field-level encryption for sensitive data
- FHIR integration via fhir/ (resources, serializers, views)
- Stripe integration for billing (billing/stripe/)
- AI features must use config/settings/ai.py for safety controls

## Developer Workflow
- **Setup:**
	- `pip install -r requirements.txt` (or use pyproject.toml)
	- Copy .env.example to .env and configure secrets
- **Run:**
	- `python manage.py migrate` (DB setup)
	- `python manage.py runserver` (dev server)
- **Test:**
	- `pytest` or `python manage.py test` (unit/integration)
- **Celery:**
	- `celery -A config worker` (background jobs)
- **Build/Deploy:**
	- Use environment-specific settings in config/settings/

## Conventions & Patterns
- No business logic in config/ (only wiring, settings, middleware registration)
- All models must support tenant isolation and audit (see common/models.py)
- Use field-level encryption for PHI
- RBAC and permission checks required for all sensitive endpoints
- Audit logs are immutable and automatically captured
- All external integrations (Stripe, FHIR, AI) must be abstracted and tested
- NO PHI in CMS (cms/README.md)

## Key Files & Directories
- config/settings/ (security, auth, logging, DB, AI, FHIR)
- common/encryption.py, audit.py, permissions.py
- tenants/models.py, middleware.py
- users/models.py, roles.py, permissions.py
- patients/models.py
- audit_logs/models.py, middleware.py
- billing/stripe/
- ai/deidentification.py, summarisation.py
- fhir/resources/
- compliance/consent.py, retention.py
- tests/

## Security Requirements
- Never commit secrets, API keys, or credentials to version control
- Use environment variables for configuration
- Implement proper input validation and sanitization
- Follow OWASP security best practices for healthcare applications

## Next Steps for AI Agents
- Update this file as new patterns emerge
- Document any non-obvious workflows, integration points, or conventions
- Reference specific files when describing patterns
