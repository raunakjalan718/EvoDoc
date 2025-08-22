from django.db import models
from core.models import TimeStampedModel
from accounts.models import User

class Appointment(TimeStampedModel):
    """Model for patient-doctor appointments"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(default=30)  # in minutes
    appointment_type = models.CharField(
        max_length=20,
        choices=[
            ('in_person', 'In-Person'),
            ('video', 'Video Consultation'),
            ('phone', 'Phone Call'),
        ],
        default='in_person'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
        ],
        default='scheduled'
    )
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} with Dr. {self.doctor.last_name} on {self.date} at {self.time}"

class AppointmentReminder(TimeStampedModel):
    """Model for appointment reminders"""
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Reminder for {self.appointment}"
