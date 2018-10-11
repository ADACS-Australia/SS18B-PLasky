from accounts.mailer import email
from accounts.utility import get_absolute_site_url

from ..display_names import (
    ERROR,
    ERROR_DISPLAY,
    WALL_TIME_EXCEEDED,
    WALL_TIME_EXCEEDED_DISPLAY,
    OUT_OF_MEMORY,
    OUT_OF_MEMORY_DISPLAY,
)

from . import templates


def email_notification_job_done(job):
    job_completion_status = 'Success'

    if job.status == ERROR:
        job_completion_status = ERROR_DISPLAY
    elif job.status == WALL_TIME_EXCEEDED:
        job_completion_status = WALL_TIME_EXCEEDED_DISPLAY + ' Error'
    elif job.status == OUT_OF_MEMORY:
        job_completion_status = OUT_OF_MEMORY_DISPLAY + ' Error'

    context = {
        'first_name': job.user.first_name,
        'last_name': job.user.last_name,
        'link': get_absolute_site_url() + '/job/' + str(job.pk),
        'job_status': job_completion_status,
    }

    email.Email(
        subject=templates.JOB_COMPLETION['subject'].format(job_completion_status),
        to_addresses=[job.user.email],
        template=templates.JOB_COMPLETION['message'],
        context=context,
    ).send_email()
