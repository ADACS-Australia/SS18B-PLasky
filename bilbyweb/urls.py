from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import common
from .views.job import job, jobs

urlpatterns = [
    path('', common.index, name='index'),
    path('about/', common.about, name='about'),
    path('new_job/', login_required(job.new_job), name='new_job'),
    path('edit_job/<job_id>/', login_required(jobs.edit_job), name='edit_job'),
    path('copy_job/<job_id>/', login_required(jobs.copy_job), name='copy_job'),
    path('delete_job/<job_id>/', login_required(jobs.delete_job), name='delete_job'),
    path('make_job_private/<job_id>/', login_required(jobs.make_job_private), name='make_job_private'),
    path('make_job_public/<job_id>/', login_required(jobs.make_job_public), name='make_job_public'),
    path('job/<job_id>/', login_required(jobs.view_job), name='job'),
    path('jobs/', jobs.jobs, name='jobs'),
    path('public_jobs/', jobs.public_jobs, name='public_jobs'),
    path('drafts/', jobs.drafts, name='drafts'),
]
