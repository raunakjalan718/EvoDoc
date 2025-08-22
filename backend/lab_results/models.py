from django.db import models
from core.models import TimeStampedModel
from accounts.models import User

class LabTest(TimeStampedModel):
    """Model for different types of lab tests"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    normal_range = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class LabResult(TimeStampedModel):
    """Model for patient lab test results"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_results')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    result_date = models.DateField()
    is_abnormal = models.BooleanField(default=False)
    lab_name = models.CharField(max_length=255, blank=True, null=True)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='ordered_lab_results'
    )
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='lab_results/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.test.name} - {self.result_date}"
