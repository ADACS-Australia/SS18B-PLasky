"""
Distributed under the MIT License. See LICENSE.txt for more info.
"""

import logging

from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from accounts.decorators import admin_or_system_admin_required

from ...utility.constants import JOBS_PER_PAGE
from ...utility.utils import get_readable_size
from ...utility.job import BilbyJob
from ...utility.display_names import (
    DRAFT,
    PUBLIC,
    NONE,
)
from ...models import Job, JobStatus


logger = logging.getLogger(__name__)


@login_required
def public_jobs(request):
    """
    Collects all public jobs and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.filter(Q(extra_status__in=[PUBLIC, ])) \
        .order_by('-last_updated', '-job_pending_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
            'public': True,
        }
    )


@login_required
def jobs(request):
    """
    Collects all jobs that are not draft or deleted and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.filter(user=request.user) \
        .exclude(job_status__in=[JobStatus.DRAFT, JobStatus.DELETED]) \
        .order_by('-last_updated', '-job_pending_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
        }
    )


@login_required
@admin_or_system_admin_required
def all_jobs(request):
    """
    Collects all jobs that are not deleted or draft and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.all() \
        .exclude(job_status__in=[JobStatus.DRAFT, JobStatus.DELETED]) \
        .order_by('-last_updated', '-job_pending_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
            'admin_view': True,
        }
    )


@login_required
def drafts(request):
    """
    Collects all drafts of the user and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.filter(Q(user=request.user), Q(job_status__in=[JobStatus.DRAFT, ])) \
        .exclude(job_status__in=[JobStatus.DELETED, ]) \
        .order_by('-last_updated', '-creation_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
            'drafts': True,
        }
    )


@login_required
@admin_or_system_admin_required
def all_drafts(request):
    """
    Collects all drafts and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.filter(Q(job_status__in=[JobStatus.DRAFT, ])) \
        .exclude(job_status__in=[JobStatus.DELETED, ]) \
        .order_by('-last_updated', '-creation_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
            'drafts': True,
            'admin_view': True,
        }
    )


@login_required
def deleted_jobs(request):
    """
    Collects all deleted jobs of the user and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.filter(Q(user=request.user), Q(job_status__in=[JobStatus.DELETED, ])) \
        .order_by('-last_updated', '-creation_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
            'deleted': True,
        }
    )


@login_required
@admin_or_system_admin_required
def all_deleted_jobs(request):
    """
    Collects all deleted jobs and renders them in template.
    :param request: Django request object.
    :return: Rendered template.
    """

    my_jobs = Job.objects.filter(Q(job_status__in=[JobStatus.DELETED, ])) \
        .order_by('-last_updated', '-creation_time')

    paginator = Paginator(my_jobs, JOBS_PER_PAGE)

    page = request.GET.get('page')
    job_list = paginator.get_page(page)

    # creating bilby jobs from jobs
    # it will create a light job with list of actions this user can do based on the job status
    bilby_jobs = []
    for job in job_list:
        bilby_job = job.bilby_job
        bilby_job.list_actions(request.user)
        bilby_jobs.append(bilby_job)

    return render(
        request,
        "bilbyweb/job/all-jobs.html",
        {
            'jobs': bilby_jobs,
            'deleted': True,
            'admin_view': True,
        }
    )


@login_required
def download_asset(request, job_id, download, file_path):
    """
    Returns a file from the server for the specified job

    :param request: The django request object
    :param job_id: int: The job id
    :param download: int: Force download or not
    :param file_path: string: the path to the file to fetch

    :return: A HttpStreamingResponse object representing the file
    """
    # Get the job
    job = get_object_or_404(Job, id=job_id)

    # Check that this user has access to this job
    # it can download assets if there is a copy access
    bilby_job = job.bilby_job
    bilby_job.list_actions(request.user)

    if 'copy' not in bilby_job.job_actions:
        # Nothing to see here
        raise Http404

    # Get the requested file from the server
    try:
        return job.fetch_remote_file(file_path, force_download=download == 1)
    except:
        raise Http404


@login_required
def view_job(request, job_id):
    """
    Collects a particular job information and renders them in template.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Rendered template.
    """

    job = None

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            # Check that this user has access to this job
            # it can view if there is a copy access
            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            if 'copy' not in bilby_job.job_actions:
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
                    # for drafts there are no clusters assigned, so bilby_job.job.custer is None for them
                    'is_online': bilby_job.job.cluster is not None and bilby_job.job.cluster.is_connected() is not None
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
                            size = get_readable_size(result.pop_ulong())

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

    if not job:
        # should return to a page notifying that no permission to view
        raise Http404


@login_required
def copy_job(request, job_id):
    """
    Copies a particular job as a draft.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Redirects to relevant view.
    """

    job = None

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            # Check whether user can copy the job
            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            if 'copy' not in bilby_job.job_actions:
                job = None
            else:
                # create a bilby_job instance of the job
                bilby_job = BilbyJob(job_id=job.id)
                job = bilby_job.clone_as_draft(request.user)
                if not job:
                    logger.info('Cannot copy job due to name length, job id: {}'.format(bilby_job.job.id))
                    # should return error about name length
                    pass
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not job:
        # should return to a page notifying that no permission to copy
        raise Http404
    else:

        # loading job as draft and redirecting to the new job view
        request.session['to_load'] = job.as_json()

    return redirect('new_job')


@login_required
def edit_job(request, job_id):
    """
    Checks job permission for edit and then redirects to relevant view.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Redirects to relevant view.
    """

    job = None

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            # Checks the edit permission for the user
            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            if 'edit' not in bilby_job.job_actions:
                job = None
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not job:
        # should return to a page notifying that no permission to edit
        raise Http404
    else:

        # loading job as draft and redirecting to the new job view
        request.session['to_load'] = job.as_json()

    return redirect('new_job')


@login_required
def cancel_job(request, job_id):
    """
    Cancels the current job.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Redirects to relevant view.
    """

    should_redirect = False

    # to decide which page to forward if not coming from any http referrer.
    # this happens when you type in the url.
    to_page = 'jobs'

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            # Checks that user has cancel permission
            if 'cancel' not in bilby_job.job_actions:
                should_redirect = False
            else:
                # Cancel the job
                job.cancel()

                should_redirect = True
        except Job.DoesNotExist:
            pass

    # this should be the last line before redirect
    if not should_redirect:
        # should return to a page notifying that no permission to cancel
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
    """
    Deletes or marks a job as deleted.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Redirects to relevant view.
    """

    should_redirect = False
    # to decide which page to forward if not coming from any http referrer.
    # this happens when you type in the url.
    to_page = 'drafts'

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            # checks that user has delete permission
            if 'delete' not in bilby_job.job_actions:
                should_redirect = False
            else:

                message = 'Job <strong>{name}</strong> has been successfully deleted'.format(name=job.name)

                if job.status == DRAFT:

                    # draft jobs are to be deleted forever as they do not have any connection with the cluster yet.
                    job.delete()

                else:

                    # for other jobs, they are marked as deleting and control is handed over to the workflow.
                    job.delete_job()

                    # cancelling the public status if deleted
                    job.extra_status = NONE
                    job.save()

                    to_page = 'jobs'

                messages.add_message(request, messages.SUCCESS, message, extra_tags='safe')
                should_redirect = True

        except Job.DoesNotExist:
            pass

    if not should_redirect:
        # should return to a page notifying that no permission to delete
        raise Http404

    # returning to the right page with pagination on
    page = 1
    full_path = request.META.get('HTTP_REFERER', None)
    if full_path and ('/drafts/' in full_path or '/jobs/' in full_path or '/public_jobs/' in full_path):
        if '?' in full_path:
            query_string = full_path.split('?')[1].split('&')
            for q in query_string:
                if q.startswith('page='):
                    page = q.split('=')[1]

        # redirect to the correct url
        if '/drafts/' in full_path:
            response = redirect('drafts')
        elif '/public_jobs/' in full_path:
            response = redirect('public_jobs')
        else:
            response = redirect('jobs')

        response['Location'] += '?page={0}'.format(page)

    else:
        response = redirect(to_page)

    return response


@login_required
def make_job_private(request, job_id):
    """
    Marks a job as private if public.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Redirects to the referrer page.
    """

    full_path = request.META.get('HTTP_REFERER', None)

    if not full_path:
        # not from a referrer, sorry
        raise Http404

    should_redirect = False

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            # Checks that user has make_it_private permission
            if 'make_it_private' in bilby_job.job_actions:
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
    """
    Marks a job as public if private.
    :param request: Django request object.
    :param job_id: id of the job.
    :return: Redirects to the referrer page.
    """
    full_path = request.META.get('HTTP_REFERER', None)

    if not full_path:
        # not from a referrer, sorry
        raise Http404

    should_redirect = False

    # checking:
    # 1. Job ID and job exists
    if job_id:
        try:
            job = Job.objects.get(id=job_id)

            bilby_job = job.bilby_job
            bilby_job.list_actions(request.user)

            # Checks that user has make_it_public permission
            if 'make_it_public' in bilby_job.job_actions:
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
