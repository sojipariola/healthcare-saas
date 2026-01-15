from django.http import Http404, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from patients.models import Patient
from .utils import patient_to_fhir

@require_http_methods(["GET"])
def patient_read(request, pk):
    """Return a FHIR Patient resource for the given patient and tenant."""
    tenant_id = request.GET.get("tenant_id")
    if not tenant_id:
        return HttpResponseBadRequest("tenant_id is required")

    try:
        patient = (
            Patient.objects.select_related("tenant")
            .only(
                "id",
                "tenant_id",
                "first_name",
                "last_name",
                "date_of_birth",
                "email",
                "phone",
            )
            .get(pk=pk, tenant_id=tenant_id)
        )
    except Patient.DoesNotExist as exc:
        raise Http404("Patient not found") from exc

    resource = patient_to_fhir(patient)
    return JsonResponse(
        resource,
        status=200,
        json_dumps_params={"indent": 2},
        content_type="application/fhir+json",
    )
