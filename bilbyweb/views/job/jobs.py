from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from ...utility.job import BilbyJob
from ...utility.display_names import (
    DELETED,
    DRAFT,
    PUBLIC,
    SUBMITTED,
    QUEUED,
    IN_PROGRESS,
    NONE,
    COMPLETED,
    ERROR,
    CANCELLING,
    CANCELLED,
    WALL_TIME_EXCEEDED,
    OUT_OF_MEMORY,
    PENDING,
    SUBMITTING,
)
from ...models import Job, JobStatus


@login_required
def public_jobs(request):
    my_jobs = Job.objects.filter(Q(extra_status__in=[PUBLIC, ])).order_by('-last_updated', '-job_pending_time')
    paginator = Paginator(my_jobs, 5)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': job_list,
            'public': True,
        }
    )


@login_required
def jobs(request):
    my_jobs = Job.objects.filter(user=request.user) \
        .exclude(job_status__in=[JobStatus.DRAFT, JobStatus.DELETED]) \
        .order_by('-last_updated', '-job_pending_time')
    paginator = Paginator(my_jobs, 5)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': job_list,
        }
    )


@login_required
def drafts(request):
    my_jobs = Job.objects.filter(Q(user=request.user), Q(job_status__in=[JobStatus.DRAFT, ])) \
        .exclude(job_status__in=[DELETED, ]).order_by('-last_updated', '-creation_time')

    paginator = Paginator(my_jobs, 5)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': job_list,
            'drafts': True,
        }
    )


@login_required
def download_asset(request, job_id, download, file_path):
    """
    Returns a file from the server for the specified job

    :param request: The django request object
    :param job_id: int: The job id
    :param file_path: string: the path to the file to fetch

    :return: A HttpStreamingResponse object representing the file
    """
    # Get the job
    job = get_object_or_404(Job, id=job_id)

    # Check that this user has access to this job
    if not (job.status == PUBLIC or request.user == job.user or request.user.is_admin()):
        # Nothing to see here
        raise Http404

    # Get the requested file from the server
    try:
        return job.fetch_remote_file(file_path, force_download=download == 1)
    except:
        raise Http404


@login_required
def view_job(request, job_id):
    # checking:
    # 1. Job ID and job exists

    job = None
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if not (job.status == PUBLIC or request.user == job.user or request.user.is_admin()):
                job = None
            else:
                # create a bilby_job instance of the job
                bilby_job = BilbyJob(job_id=job.id)
                bilby_job.list_actions(request.user)

                # Empty parameter dict to pass to template
                job_data = {
                    'L1': None,
                    'V1': None,
                    'H1': None,
                    'corner': None,
                    'archive': None,
                    'is_online': bilby_job.job.cluster.is_connected() is not None
                }

                # Check if the cluster is online
                if job_data['is_online']:
                    try:
                        # Get the output file list for this job
                        result = bilby_job.job.fetch_remote_file_list(path="/", recursive=True)
                        # Waste the message id
                        result.pop_uint()
                        # Iterate over each file
                        num_entries = result.pop_uint()
                        for _ in range(num_entries):
                            path = result.pop_string()
                            # Waste the is_file bool
                            result.pop_bool()
                            # Waste the file size
                            size = result.pop_ulong()

                            # Check if this is a wanted file
                            if 'output/L1_frequency_domain_data.png' in path:
                                job_data['L1'] = {'path': path, 'size': size}
                            if 'output/V1_frequency_domain_data.png' in path:
                                job_data['V1'] = {'path': path, 'size': size}
                            if 'output/H1_frequency_domain_data.png' in path:
                                job_data['H1'] = {'path': path, 'size': size}
                            if 'output/bilby_corner.png' in path:
                                job_data['corner'] = {'path': path, 'size': size}
                            if 'bilby_job_{}.tar.gz'.format(bilby_job.job.id) in path:
                                job_data['archive'] = {'path': path, 'size': size}
                    except:
                        job_data['is_online'] = False

                return render(
                    request,
                    "bilbyweb/job/view_job.html",
                    {
                        'bilby_job': bilby_job,
                        'job_data': job_data
                    }
                )
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
                # create a bilby_job instance of the job
                bilby_job = BilbyJob(job_id=job.id)
                job = bilby_job.clone_as_draft(request.user)
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
def cancel_job(request, job_id):
    # checking:
    # 1. Job ID and job exists

    job = None

    should_redirect = False

    # to decide which page to forward if not coming from any http referrer.
    # this happens when you type in the url.
    to_page = 'jobs'

    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            # permission check and
            # status check, whether cancel is allowed for the job
            if not (request.user == job.user or request.user.is_admin()) or \
                    job.status not in [PENDING, SUBMITTING, SUBMITTED, QUEUED, IN_PROGRESS]:
                should_redirect = False
            else:
                # TODO
                # job.status = CANCELLING
                # job.save()
                pass
                should_redirect = True
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not should_redirect:
        # should return to a page notifying that no permission to view the job or no job or job not in correct status
        raise Http404

    # returning to the right page with pagination on
    page = 1
    full_path = request.META.get('HTTP_REFERER', None)
    if full_path:
        if '/jobs/' in full_path:
            if '?' in full_path:
                query_string = full_path.split('?')[1].split('&')
                for q in query_string:
                    if q.startswith('page='):
                        page = q.split('=')[1]

            response = redirect('jobs')
            response['Location'] += '?page={0}'.format(page)
        else:
            response = redirect(full_path)
    else:
        response = redirect(to_page)

    return response


@login_required
def delete_job(request, job_id):
    # checking:
    # 1. Job ID and job exists

    should_redirect = False
    # to decide which page to forward if not coming from any http referrer.
    # this happens when you type in the url.
    to_page = 'drafts'
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if not (request.user == job.user or request.user.is_admin()) or \
                    job.status not in [DRAFT, COMPLETED, ERROR, CANCELLED, WALL_TIME_EXCEEDED, OUT_OF_MEMORY, PUBLIC]:
                should_redirect = False
            else:
                message = 'Job <strong>{name}</strong> has been successfully deleted'.format(name=job.name)
                if job.status == DRAFT:
                    job.delete()
                else:
                    job.extra_status = DELETED
                    job.save()
                    to_page = 'jobs'
                messages.add_message(request, messages.SUCCESS, message, extra_tags='safe')
                should_redirect = True
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not should_redirect:
        # should return to a page notifying that no permission to view the job or no job or job not in draft
        raise Http404

    # returning to the right page with pagination on
    page = 1
    full_path = request.META.get('HTTP_REFERER', None)
    if full_path and ('/drafts/' in full_path or '/jobs/' in full_path):
        if '?' in full_path:
            query_string = full_path.split('?')[1].split('&')
            for q in query_string:
                if q.startswith('page='):
                    page = q.split('=')[1]

        response = redirect('drafts') if '/drafts/' in full_path else redirect('jobs')
        response['Location'] += '?page={0}'.format(page)
    else:
        response = redirect(to_page)

    return response


@login_required
def make_job_private(request, job_id):
    full_path = request.META.get('HTTP_REFERER', None)
    if not full_path:
        raise Http404

    # checking:
    # 1. Job ID and job exists

    should_redirect = False
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if job.status == PUBLIC and (request.user == job.user or request.user.is_admin()):
                job.extra_status = NONE
                job.save()
                should_redirect = True
                messages.success(request, 'Job has been changed to <strong>private!</strong>', extra_tags='safe')
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not should_redirect:
        # should return to a page notifying that
        # 1. no permission to view the job or
        # 2. no job or
        # 3. job does not have correct status
        raise Http404

    return redirect(full_path)


@login_required
def make_job_public(request, job_id):
    full_path = request.META.get('HTTP_REFERER', None)
    if not full_path:
        raise Http404

    # checking:
    # 1. Job ID and job exists

    should_redirect = False
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            if job.status == COMPLETED and (request.user == job.user or request.user.is_admin()):
                job.extra_status = PUBLIC
                job.save()
                should_redirect = True
                messages.success(request, 'Job has been changed to <strong>public!</strong>', extra_tags='safe')
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not should_redirect:
        # should return to a page notifying that
        # 1. no permission to view the job or
        # 2. no job or
        # 3. job does not have correct status
        raise Http404

    return redirect(full_path)
