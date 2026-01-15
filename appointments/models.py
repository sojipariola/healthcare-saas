

from django.db import models
from patients.models import Patient
from tenants.models import Tenant
# from users.models import User

class Appointment(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="appointments")
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
	scheduled_for = models.DateTimeField()
	status = models.CharField(max_length=20, default="scheduled")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.patient} @ {self.scheduled_for}"

####################################################################################################
'''class DoctorAvailability(models.Model):
	tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="doctor_availabilities")
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="availabilities", limit_choices_to={"roles__name": "doctor"}, )
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	class Meta:
		unique_together = ("doctor", "start_time", "end_time")

	def __str__(self):
		return f"{self.doctor} available from {self.start_time} to {self.end_time}"

class AppointmentDoctorAssignment(models.Model):
	appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="doctor_assignment")
	doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_as_doctor", limit_choices_to={"roles__name": "doctor"}, )
	def __str__(self):
		return f"Appointment {self.appointment.id} assigned to Dr. {self.doctor}"'''