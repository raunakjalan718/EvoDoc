from django.contrib import admin
from .models import Review, SideEffect, MedicationReview

class SideEffectInline(admin.TabularInline):
    model = SideEffect
    extra = 1

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'get_treatment_name', 'effectiveness_rating', 'side_effects_severity', 'created_at')
    search_fields = ('patient__username', 'treatment__treatment__name')
    inlines = [SideEffectInline]
    
    def get_treatment_name(self, obj):
        return obj.treatment.treatment.name
    get_treatment_name.short_description = 'Treatment'
    get_treatment_name.admin_order_field = 'treatment__treatment__name'

@admin.register(MedicationReview)
class MedicationReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medication', 'effectiveness_rating', 'side_effects_experienced', 'created_at')
    list_filter = ('side_effects_experienced',)
    search_fields = ('patient__username', 'medication__name')
