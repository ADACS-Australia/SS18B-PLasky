from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import index, job

urlpatterns = [
    path('', index.index, name='index'),
    path('about/', index.index, name='about'),
    path('new_job/', login_required(job.job_start), name='job_start'),
    path('jobs/', index.index, name='job_list'),
]
