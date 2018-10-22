"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from bilbyweb.models import Job
from bilbyweb.utility.display_names import (
    COMPLETED,
    ERROR,
    WALL_TIME_EXCEEDED,
    OUT_OF_MEMORY,
)

from .utility.email.email import email_notification_job_done


@receiver(pre_save, sender=Job, dispatch_uid='update_last_updated')
def update_last_updated(instance, **kwargs):
    """
    Signal to update the last updated for the Job
    :param instance: instance of Job
    :param kwargs: keyward arguments
    :return: Nothing
    """
    if instance.pk:
        instance.last_updated = timezone.now()


@receiver(pre_save, sender=Job, dispatch_uid='notify_job_owner')
def notify_job_owner(instance, **kwargs):
    """
    Signal to send email notification on Job finished processing
    :param instance: instance of Job
    :param kwargs: keyward arguments
    :return: Nothing
    """
    if instance.pk:

        # finding the actual instance
        old_instance = Job.objects.get(pk=instance.pk)

        # checking whether a status change happened
        # it should check on the actual number, not the status property as that will
        # cause problems for changing from public to private and vice versa
        if instance.job_status != old_instance.job_status:

            # checking whether we need to send a notification email
            if instance.status in [COMPLETED, ERROR, WALL_TIME_EXCEEDED, OUT_OF_MEMORY]:

                # sending email notification to the user
                email_notification_job_done(instance)
