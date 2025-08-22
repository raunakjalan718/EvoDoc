from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    """Base model with created and modified timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class SoftDeleteModel(models.Model):
    """Base model with soft delete functionality"""
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
    
    class Meta:
        abstract = True
