from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

from bilbyweb.models import Job


@receiver(pre_save, sender=Job, dispatch_uid='update_last_updated')
def update_last_updated(instance, **kwargs):
    if instance.pk:
        instance.last_updated = timezone.now()
