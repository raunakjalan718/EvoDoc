from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from medical.models import PatientProfile, DoctorProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'patient':
            PatientProfile.objects.create(user=instance)
        elif instance.user_type == 'doctor':
            DoctorProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'patient':
        if hasattr(instance, 'patient_profile'):
            instance.patient_profile.save()
        else:
            PatientProfile.objects.create(user=instance)
    elif instance.user_type == 'doctor':
        if hasattr(instance, 'doctor_profile'):
            instance.doctor_profile.save()
        else:
            DoctorProfile.objects.create(user=instance)
