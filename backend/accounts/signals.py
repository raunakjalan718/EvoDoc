from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

# We'll implement additional profile creation logic later
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # This will be expanded when we create specific Patient and Doctor models
        pass
