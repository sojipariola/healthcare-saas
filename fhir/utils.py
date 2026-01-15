def patient_to_fhir(patient):
    """Map internal Patient to a FHIR Patient resource."""
    telecom = []
    if patient.phone:
        telecom.append({"system": "phone", "value": patient.phone, "use": "mobile"})
    if patient.email:
        telecom.append({"system": "email", "value": patient.email})

    return {
        "resourceType": "Patient",
        "id": str(patient.pk),
        "meta": {
            "profile": ["http://hl7.org/fhir/StructureDefinition/Patient"],
        },
        "identifier": [
            {
                "system": "urn:healthcare-saas:tenant",
                "value": str(patient.tenant_id),
            },
            {
                "system": "urn:healthcare-saas:patient-id",
                "value": str(patient.pk),
            },
        ],
        "name": [
            {
                "family": patient.last_name or "",
                "given": [patient.first_name or ""],
            }
        ],
        "telecom": telecom,
        "birthDate": patient.date_of_birth.isoformat(),
        "managingOrganization": {
            "identifier": {
                "system": "urn:healthcare-saas:tenant",
                "value": str(patient.tenant_id),
            }
        },
    }
