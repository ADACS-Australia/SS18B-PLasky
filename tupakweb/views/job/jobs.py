from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from ...utility.job import TupakJob
from ...utility.display_names import DELETED, DRAFT, PUBLIC, SUBMITTED, QUEUED, IN_PROGRESS
from ...models import Job


@login_required
def jobs(request):
    my_jobs = Job.objects.filter(Q(user=request.user), ~Q(status__in=[DELETED, DRAFT, ])).order_by('-last_updated',
                                                                                                   '-submission_time')
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


@login_required
def drafts(request):
    my_jobs = Job.objects.filter(Q(user=request.user), Q(status__in=[DRAFT, ])).order_by('-last_updated',
                                                                                         '-creation_time')
    paginator = Paginator(my_jobs, 5)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    return render(
        request,
        "tupakweb/job/all-jobs.html",
        {
            'jobs': job_list,
            'drafts': True,
        }
    )


@login_required
def copy_job(request, job_id):
    # checking:
    # 1. Job ID and job exists

    job = None
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if not (job.status == PUBLIC or request.user == job.user or request.user.is_admin()):
                job = None
            else:
                # create a tupak_job instance of the job
                tupak_job = TupakJob(job_id=job.id)
                job = tupak_job.clone_as_draft(request.user)
                if not job:
                    print('cannot copy due to name length')
                    # should return error about name length
                    pass
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not job:
        # should return to a page notifying that no permission to view the job or no job or job not in draft
        raise Http404
    else:
        request.session['to_load'] = job.as_json()

    return redirect('new_job')


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
        raise Http404
    else:
        request.session['to_load'] = job.as_json()

    return redirect('new_job')


@login_required
def delete_job(request, job_id):
    # checking:
    # 1. Job ID and job exists

    should_redirect = False
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if not (request.user == job.user or request.user.is_admin()) or job.status in [SUBMITTED, QUEUED,
                                                                                           IN_PROGRESS, DELETED]:
                should_redirect = False
            else:
                if job.status == DRAFT:
                    job.delete()
                else:
                    job.status = DELETED
                    job.save()
                should_redirect = True
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not should_redirect:
        # should return to a page notifying that no permission to view the job or no job or job not in draft
        raise Http404

    # returning to the right page with pagination on
    page = 1
    full_path = request.META.get('HTTP_REFERER')
    if '?' in full_path:
        query_string = full_path.split('?')[1].split('&')
        for q in query_string:
            if q.startswith('page='):
                page = q.split('=')[1]

    response = redirect('drafts') if '/drafts/' in full_path else redirect('jobs')
    response['Location'] += '?page={0}'.format(page)
    return response
