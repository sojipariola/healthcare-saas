from django.apps import AppConfig

class FhirConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fhir"
    verbose_name = "FHIR Interoperability"
