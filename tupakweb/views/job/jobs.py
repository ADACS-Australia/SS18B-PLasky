from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from ...models import Job


@login_required
def jobs(request):
    my_jobs = Job.objects.filter(Q(user=request.user), ~Q(status__in=[Job.DELETED, ])).order_by('-submission_time',
                                                                                                '-creation_time')
    paginator = Paginator(my_jobs, 5)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    return render(
        request,
        "tupakweb/job/all-jobs.html",
        {
            'jobs': job_list,
        }
    )
