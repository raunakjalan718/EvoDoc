from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from accounts.models import User

class Condition(TimeStampedModel, SoftDeleteModel):
    """Model for medical conditions/diseases"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icd10_code = models.CharField(max_length=10, blank=True, null=True)  # Standard medical classification code
    
    def __str__(self):
        return self.name

class Allergy(TimeStampedModel, SoftDeleteModel):
    """Model for allergies"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Medication(TimeStampedModel, SoftDeleteModel):
    """Model for medications"""
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    dosage_form = models.CharField(max_length=100, blank=True, null=True)  # e.g., tablet, capsule, liquid
    strength = models.CharField(max_length=100, blank=True, null=True)  # e.g., 500mg, 10ml
    
    def __str__(self):
        return self.name

class PatientProfile(TimeStampedModel):
    """Extended profile for patients"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)  # in cm
    weight = models.FloatField(blank=True, null=True)  # in kg
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"Patient: {self.user.username}"

class DoctorProfile(TimeStampedModel):
    """Extended profile for doctors"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name() or self.user.username}"

class PatientCondition(TimeStampedModel):
    """Model for linking patients to conditions"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conditions')
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    diagnosed_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('active', 'Active'),
            ('resolved', 'Resolved'),
            ('in_remission', 'In Remission'),
            ('chronic', 'Chronic'),
        ],
        default='active'
    )
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.condition.name}"

class PatientAllergy(TimeStampedModel):
    """Model for linking patients to allergies"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allergies')
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
        ],
        default='mild'
    )
    reaction = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.allergy.name}"

class PatientMedication(TimeStampedModel):
    """Model for linking patients to medications"""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    prescribed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='prescribed_medications'
    )
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient.username} - {self.medication.name}"
