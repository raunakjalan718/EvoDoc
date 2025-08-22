from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from accounts.models import User
from medical.models import Condition, Medication

class Treatment(TimeStampedModel, SoftDeleteModel):
    """Model for medical treatments"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    conditions = models.ManyToManyField(Condition, related_name='treatments')
    medications = models.ManyToManyField(Medication, related_name='treatments', blank=True)
    duration = models.CharField(max_length=100, blank=True, null=True)  # e.g., "7 days", "2 weeks"
    
    def __str__(self):
        return self.name

class PatientTreatment(TimeStampedModel):
    """Model for linking patients to treatments"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='treatments')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    prescribed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='prescribed_treatments'
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('discontinued', 'Discontinued'),
        ],
        default='active'
    )
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.treatment.name}"
