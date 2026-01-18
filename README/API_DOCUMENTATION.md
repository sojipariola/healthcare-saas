# ClinicCloud API Documentation

## Overview
The ClinicCloud API is a RESTful API built with Django REST Framework, providing complete access to healthcare data with JWT authentication and multi-tenant support.

## Base URL
- **Development**: `http://localhost:8000/api/v1/`
- **Production**: `https://healthcare-saas-app.herokuapp.com/api/v1/`

## Authentication

All API requests require JWT authentication.

### Get Access Token
```bash
POST /api/v1/auth/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Use Token in Requests
```bash
Authorization: Bearer <access_token>
```

### Refresh Token
```bash
POST /api/v1/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

## Endpoints

### Authentication
- `POST /api/v1/auth/token/` - Obtain JWT tokens
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `GET /api/v1/auth/me/` - Get current user info
- `POST /api/v1/auth/logout/` - Logout (optional)
- `POST /api/v1/auth/register/` - Register new user

### Patients
- `GET /api/v1/patients/` - List all patients
- `POST /api/v1/patients/` - Create new patient
- `GET /api/v1/patients/{id}/` - Get patient details
- `PUT /api/v1/patients/{id}/` - Update patient
- `DELETE /api/v1/patients/{id}/` - Delete patient
- `GET /api/v1/patients/{id}/appointments/` - Get patient's appointments
- `GET /api/v1/patients/{id}/clinical_records/` - Get patient's clinical records

### Appointments
- `GET /api/v1/appointments/` - List appointments
- `POST /api/v1/appointments/` - Create appointment
- `GET /api/v1/appointments/{id}/` - Get appointment details
- `PUT /api/v1/appointments/{id}/` - Update appointment
- `DELETE /api/v1/appointments/{id}/` - Delete appointment
- `GET /api/v1/appointments/today/` - Get today's appointments
- `GET /api/v1/appointments/upcoming/` - Get upcoming appointments (next 7 days)

### Clinical Records
- `GET /api/v1/clinical-records/` - List clinical records
- `POST /api/v1/clinical-records/` - Create SOAP note
- `GET /api/v1/clinical-records/{id}/` - Get record details
- `PUT /api/v1/clinical-records/{id}/` - Update record
- `POST /api/v1/clinical-records/{id}/lock/` - Lock record (immutable)

### Lab Results
- `GET /api/v1/lab-results/` - List lab results
- `POST /api/v1/lab-results/` - Create lab result
- `GET /api/v1/lab-results/{id}/` - Get result details

### Dashboard
- `GET /api/v1/dashboard/stats/` - Get dashboard statistics

## Query Parameters

### Pagination
```
GET /api/v1/patients/?page=2&page_size=50
```

### Filtering
```
GET /api/v1/appointments/?date_from=2024-01-01&date_to=2024-01-31&status=scheduled
```

### Search
```
GET /api/v1/patients/?search=John
```

### Ordering
```
GET /api/v1/patients/?ordering=-created_at
```

## Response Format

### Success Response (200 OK)
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "date_of_birth": "1990-01-01",
  "gender": "M",
  "is_active": true,
  "created_at": "2024-01-17T10:30:00Z",
  "updated_at": "2024-01-17T10:30:00Z"
}
```

### List Response with Pagination
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/patients/?page=2",
  "previous": null,
  "results": [
    { "id": 1, "first_name": "John", ... },
    { "id": 2, "first_name": "Jane", ... }
  ]
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "Invalid email format",
  "status": 400
}
```

## HTTP Status Codes
- `200 OK` - Request successful
- `201 Created` - Resource created
- `204 No Content` - Request successful with no response body
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., duplicate)
- `500 Server Error` - Server error

## Example Usage

### Get Patients
```bash
curl -X GET http://localhost:8000/api/v1/patients/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json"
```

### Create Patient
```bash
curl -X POST http://localhost:8000/api/v1/patients/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "phone": "555-0123"
  }'
```

### Create Appointment
```bash
curl -X POST http://localhost:8000/api/v1/appointments/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "provider": 2,
    "appointment_date": "2024-02-01",
    "appointment_time": "14:00",
    "duration_minutes": 30,
    "appointment_type": "consultation"
  }'
```

## API Documentation
- **Swagger UI**: `/api/docs/` - Interactive API documentation
- **Schema**: `/api/schema/` - OpenAPI schema

## Permissions
- Must be authenticated to access API endpoints
- Users can only access data from their tenant
- RBAC enforced on sensitive operations

## Rate Limiting
- Anonymous: 100 requests/hour
- Authenticated: 1000 requests/hour

## CORS
API is accessible from:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)
- Production domains (configured via environment variables)
