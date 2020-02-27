from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Organization


@receiver(post_save, sender=Organization)
def create_organization(sender, instance, created, **kwargs):
    """
    "owner" field should be required in admin form, and in user form
     it should be automatically set. Field "created_by" should be
     automatically set in user form, but it will be read only in admin
     form so "created_by" is being set to "owner" here.
     "owner" is also being added here to organization's "members" and
     "administrators".
    """
    if created:
        if not instance.created_by:
            instance.created_by = instance.owner
        instance.administrators.add(instance.owner)
        instance.members.add(instance.owner)
        instance.save()
