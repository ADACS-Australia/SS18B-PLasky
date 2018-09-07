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
    path('jobs/', jobs.jobs, name='jobs'),
    path('drafts/', jobs.drafts, name='drafts'),
]
