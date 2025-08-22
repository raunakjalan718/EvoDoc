from django.contrib import admin
from .models import LabTest, LabResult

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'normal_range', 'unit')
    search_fields = ('name',)

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test', 'value', 'result_date', 'is_abnormal')
    list_filter = ('is_abnormal', 'result_date')
    search_fields = ('patient__username', 'test__name')
