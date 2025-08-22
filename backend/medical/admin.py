from django.contrib import admin
from .models import (
    Condition, Allergy, Medication,
    PatientProfile, DoctorProfile,
    PatientCondition, PatientAllergy, PatientMedication
)

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'icd10_code', 'is_active')
    search_fields = ('name', 'icd10_code')

@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'dosage_form', 'strength', 'is_active')
    search_fields = ('name', 'generic_name')

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'blood_group')
    search_fields = ('user__username', 'user__email')

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'license_number', 'experience_years')
    search_fields = ('user__username', 'user__email', 'specialization')

@admin.register(PatientCondition)
class PatientConditionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'condition', 'status', 'diagnosed_date')
    list_filter = ('status',)
    search_fields = ('patient__username', 'condition__name')

@admin.register(PatientAllergy)
class PatientAllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergy', 'severity')
    list_filter = ('severity',)
    search_fields = ('patient__username', 'allergy__name')

@admin.register(PatientMedication)
class PatientMedicationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medication', 'dosage', 'frequency', 'active')
    list_filter = ('active',)
    search_fields = ('patient__username', 'medication__name')
