from django.contrib import admin
from .models import Appointment, AppointmentReminder

class AppointmentReminderInline(admin.TabularInline):
    model = AppointmentReminder
    extra = 1

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'appointment_type', 'status')
    list_filter = ('status', 'appointment_type', 'date')
    search_fields = ('patient__username', 'doctor__username', 'reason')
    inlines = [AppointmentReminderInline]
