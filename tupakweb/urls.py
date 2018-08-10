from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from .views import common
from .views.job import job, jobs

urlpatterns = [
    path('', common.index, name='index'),
    path('about/', common.about, name='about'),
    path('new_job/', login_required(job.new_job), name='new_job'),
    # re_path(r'^new_job/(?P<id>\d+)/$', job.edit_job, name='job_name_edit'),
    # re_path(r'^new_job/(?P<id>\d+)/data$', job.job_data, name='job_data_edit'),
    # re_path(r'^new_job/(?P<id>\d+)/signal', job.job_signal, name='job_signal_edit'),
    # re_path(r'^new_job/(?P<id>\d+)/prior$', job.job_prior, name='job_prior_edit'),
    # re_path(r'^new_job/(?P<id>\d+)/sampler$', job.job_sampler, name='job_sampler_edit'),
    # re_path(r'^new_job/(?P<id>\d+)/launch$', job.job_launch, name='job_launch'),
    path('jobs/', jobs.jobs, name='jobs'),
]
