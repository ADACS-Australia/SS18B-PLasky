from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ...models import Job

@login_required
def jobs(request):
    my_jobs = Job.objects.filter(user=request.user)

    return render(
        request,
        "tupakweb/job/jobs.html",
        {
            'job': my_jobs,
        }
    )