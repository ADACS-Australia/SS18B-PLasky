from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import common
from .views.jobs import job

urlpatterns = [
    path('', common.index, name='index'),
    path('about/', common.about, name='about'),
    path('new_job/', login_required(job.job_start), name='job_start'),
    path('jobs/', job.jobs, name='jobs'),
]
