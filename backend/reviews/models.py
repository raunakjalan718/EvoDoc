from django.db import models
from core.models import TimeStampedModel
from accounts.models import User
from treatments.models import PatientTreatment, Treatment
from medical.models import Medication

class Review(TimeStampedModel):
    """Model for patient reviews of treatments"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    treatment = models.ForeignKey(PatientTreatment, on_delete=models.CASCADE, related_name='reviews')
    effectiveness_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    side_effects_severity = models.PositiveSmallIntegerField(
        choices=[
            (1, 'None'),
            (2, 'Mild'),
            (3, 'Moderate'),
            (4, 'Severe'),
            (5, 'Very Severe'),
        ],
        blank=True,
        null=True
    )
    side_effects_description = models.TextField(blank=True, null=True)
    time_to_effect = models.CharField(max_length=100, blank=True, null=True)  # e.g., "2 days", "1 week"
    comments = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('patient', 'treatment')
    
    def __str__(self):
        return f"Review by {self.patient.username} for {self.treatment.treatment.name}"

class SideEffect(TimeStampedModel):
    """Model for tracking specific side effects in reviews"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='side_effects')
    name = models.CharField(max_length=255)
    severity = models.PositiveSmallIntegerField(
        choices=[
            (1, 'Mild'),
            (2, 'Moderate'),
            (3, 'Severe'),
        ],
        default=1
    )
    onset_time = models.CharField(max_length=100, blank=True, null=True)  # e.g., "2 hours after taking", "next day"
    duration = models.CharField(max_length=100, blank=True, null=True)  # e.g., "2 hours", "all day"
    
    def __str__(self):
        return self.name

class MedicationReview(TimeStampedModel):
    """Model for patient reviews of specific medications"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medication_reviews')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='reviews')
    effectiveness_rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    side_effects_experienced = models.BooleanField(default=False)
    side_effects_description = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('patient', 'medication')
    
    def __str__(self):
        return f"Review by {self.patient.username} for {self.medication.name}"
