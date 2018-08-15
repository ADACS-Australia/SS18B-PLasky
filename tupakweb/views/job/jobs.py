from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from ...models import Job


@login_required
def jobs(request):
    my_jobs = Job.objects.filter(Q(user=request.user), ~Q(status__in=[Job.DELETED, ])).order_by('-submission_time',
                                                                                                '-creation_time')
    paginator = Paginator(my_jobs, 100)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    return render(
        request,
        "tupakweb/job/all-jobs.html",
        {
            'jobs': job_list,
        }
    )


@login_required
def edit_job(request, job_id):
    # checking:
    # 1. Job ID and job exists

    job = None
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if not (request.user == job.user or request.user.is_admin()):
                job = None
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not job:
        # should return to a page notifying that no permission to view the job or no job or job not in draft
        pass
    else:
        request.session['to_load'] = job.as_json()

    return redirect('new_job')
