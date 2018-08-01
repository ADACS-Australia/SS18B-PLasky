from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from ...models import Job


@login_required
def job_start(request):
    return render(
        request,
        "tupakweb/welcome.html",
    )


@login_required
def jobs(request):
    my_jobs = Job.objects.filter(Q(user=request.user), ~Q(status__in=[Job.DELETED, ]))

    return render(
        request,
        "tupakweb/job/jobs.html",
        {
            'jobs': my_jobs,
        }
    )
